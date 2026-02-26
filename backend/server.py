from fastapi import FastAPI, APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone, timedelta
import bcrypt
import jwt
import json
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Environment Configuration
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development')
IS_PRODUCTION = ENVIRONMENT == 'production'

logger.info(f"🚀 Starting in {ENVIRONMENT} mode")

# Validate required environment variables
REQUIRED_ENV_VARS = ['JWT_SECRET_KEY', 'FOUNDER_EMAIL']
missing_vars = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
if missing_vars:
    raise ValueError(f"❌ Missing required environment variables: {', '.join(missing_vars)}\n"
                     f"   Please check your .env file and add the missing values.")

# MongoDB connection (optional, with fallback to in-memory storage)
try:
    mongo_url = os.environ.get('MONGO_URL')
    if mongo_url:
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
        db = client[os.environ.get('DB_NAME', 'medcures_database')]
        logger.info("✓ MongoDB connection configured")
    else:
        db = None
        logger.warning("⚠ No MONGO_URL configured, using in-memory storage")
except Exception as e:
    db = None
    logger.warning(f"⚠ MongoDB connection failed: {e}, using in-memory storage instead")

# OpenRouter client (optional, for AI-powered responses)
try:
    openrouter_api_key = os.environ.get('OPENROUTER_API_KEY')
    if openrouter_api_key:
        openrouter_client = OpenAI(
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            timeout=10.0
        )
        logger.info("✓ OpenRouter client configured")
    else:
        openrouter_client = None
        logger.warning("⚠ No OPENROUTER_API_KEY configured")
except Exception as e:
    openrouter_client = None
    logger.warning(f"⚠ OpenRouter client initialization failed: {e}")

# JWT settings
JWT_SECRET = os.environ['JWT_SECRET_KEY']
JWT_ALGORITHM = "HS256"
FOUNDER_EMAIL = os.environ['FOUNDER_EMAIL']

# Security: Validate JWT Secret in production
if IS_PRODUCTION and len(JWT_SECRET) < 32:
    raise ValueError("❌ JWT_SECRET_KEY must be at least 32 characters in production!")

# Load pharmacopoeia data
with open(ROOT_DIR / 'pharmacopoeia.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
    if isinstance(data, dict) and "PharmacopoeiaDrugs" in data:
        drugs = data.get("PharmacopoeiaDrugs", [])
    elif isinstance(data, dict):
        # try to find the first list value if wrapped differently
        drugs = next((v for v in data.values() if isinstance(v, list)), [])
    else:
        drugs = data

    # Normalize keys: some entries use 'citation' while code expects 'citations'
    for d in drugs:
        if isinstance(d, dict):
            if "citation" in d and "citations" not in d:
                d["citations"] = d.pop("citation")
            if "citations" not in d:
                d["citations"] = []

    PHARMACOPOEIA = drugs

# In-memory user storage (for testing without MongoDB)
USERS_DB = {}

# Security
security = HTTPBearer()

app = FastAPI()
api_router = APIRouter(prefix="/api")

# ===== GLOBAL ERROR HANDLER (prevents crashes) =====
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Catch ALL errors and return proper response instead of crashing"""
    logger.error(f"❌ Unhandled error: {str(exc)}", exc_info=True)
    return {
        "error": "An unexpected error occurred",
        "message": str(exc) if not IS_PRODUCTION else "Internal server error",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    email: str
    name: str
    is_admin: bool = False
    chat_count: int = 0
    is_member: bool = False
    created_at: str

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: str
    citations: Optional[List[str]] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    citations: Optional[List[str]] = None
    drug_info: Optional[dict] = None

class FeedbackSubmit(BaseModel):
    session_id: str
    message_id: str
    rating: str  # "positive" or "negative"
    message_content: str
    response_content: str

class Feedback(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    session_id: str
    message_id: str
    rating: str
    message_content: str
    response_content: str
    timestamp: str
    user_email: Optional[str] = None

# Helper functions
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_token(user_id: str, email: str) -> str:
    payload = {
        "user_id": user_id,
        "email": email,
        "exp": datetime.now(timezone.utc) + timedelta(days=30)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    payload = verify_token(token)
    user = await db.users.find_one({"id": payload["user_id"]}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_admin_user(user: dict = Depends(get_current_user)) -> dict:
    if user["email"] != FOUNDER_EMAIL:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def search_drug(query: str) -> Optional[dict]:
    query_lower = query.lower()
    for drug in PHARMACOPOEIA:
        if drug["name"].lower() in query_lower or query_lower in drug["name"].lower():
            return drug
    return None

def get_ai_response(message: str, drug_info: Optional[dict] = None, context: str = "") -> tuple:
    system_message = """You are Medcures, a professional medical information assistant. You provide educational information about medications in a soft, professional tone.
    
IMPORTANT RULES:
1. Always add this disclaimer: "⚠️ This is for educational purposes only. Please consult a qualified healthcare professional before taking any medication."
2. Be professional, soft, and trustworthy in your tone
3. If asked about dosage, always ask for: age, sex, and preferred route of administration first
4. Provide information in well-formatted sections with proper spacing
5. Always cite sources when available
6. Never prescribe or provide medical advice
7. If you don't have specific information, say so clearly"""
    
    user_message = message
    if drug_info:
        user_message = f"""User asked: {message}
        
Here is verified information from pharmacopoeia:
Drug: {drug_info['name']}
Category: {drug_info['category']}
Route: {drug_info['route']}
Storage: {drug_info['storage']}
Dose: {drug_info['dose']}
Uses: {drug_info['uses']}
Side Effects: {drug_info['side_effects']}
Sources: {', '.join(drug_info['citations'])}

Provide a professional response using this information. Format it well with proper sections."""
    
    if context:
        user_message = context + "\n\n" + user_message
    
    try:
        response = openrouter_client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        ai_response = response.choices[0].message.content
        citations = drug_info['citations'] if drug_info else None
        
        return ai_response, citations
    except Exception as e:
        logging.error(f"OpenRouter API error: {str(e)}")
        
        # Fallback response when AI service is unavailable
        if drug_info:
            # Format dosage properly if it's a dictionary
            dosage_text = ""
            if isinstance(drug_info['dose'], dict):
                for key, value in drug_info['dose'].items():
                    dosage_text += f" • {key.capitalize()}: {value}\n"
            else:
                dosage_text = str(drug_info['dose'])
            
            # Format uses properly if it's a list
            uses_text = ""
            if isinstance(drug_info['uses'], list):
                for use in drug_info['uses']:
                    uses_text += f" • {use}\n"
            else:
                uses_text = str(drug_info['uses'])
            
            # Format side effects properly if it's a list
            side_effects_text = ""
            if isinstance(drug_info['side_effects'], list):
                for effect in drug_info['side_effects']:
                    side_effects_text += f" • {effect}\n"
            else:
                side_effects_text = str(drug_info['side_effects'])
            
            fallback_response = f"""{drug_info['name']} Information

Category: {drug_info['category']}
Route of Administration: {drug_info['route']}
Storage: {drug_info['storage']}

Dosage:
{dosage_text.strip()}

Uses:
{uses_text.strip()}

Side Effects:
{side_effects_text.strip()}

⚠️ This is for educational purposes only. Please consult a qualified healthcare professional before taking any medication.

Sources: {', '.join(drug_info['citations'])}"""
            return fallback_response, drug_info['citations']
        else:
            fallback_response = """I apologize, but I'm currently experiencing technical difficulties with my AI service. 

However, I can provide information about the following medications from my verified database:
- Aspirin (pain relief, antiplatelet)
- Paracetamol (pain relief, fever reduction)
- Amoxicillin (antibiotic)
- Ibuprofen (anti-inflammatory)

⚠️ This is for educational purposes only. Please consult a qualified healthcare professional before taking any medication."""
            return fallback_response, None

# Routes
@api_router.post("/auth/signup")
async def signup(user_data: UserCreate):
    # Check if user already exists in memory
    if user_data.email in USERS_DB:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_id = str(uuid.uuid4())
    user_doc = {
        "id": user_id,
        "email": user_data.email,
        "password": hash_password(user_data.password),
        "name": user_data.name,
        "is_admin": user_data.email == FOUNDER_EMAIL,
        "chat_count": 0,
        "is_member": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    
    # Store in memory instead of MongoDB
    USERS_DB[user_data.email] = user_doc
    
    token = create_token(user_id, user_data.email)
    
    return {
        "token": token,
        "user": {
            "id": user_id,
            "email": user_data.email,
            "name": user_data.name,
            "is_admin": user_doc["is_admin"],
            "is_member": False
        }
    }

@api_router.post("/auth/login")
async def login(credentials: UserLogin):
    # Check in memory instead of MongoDB
    user = USERS_DB.get(credentials.email)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_token(user["id"], user["email"])
    
    return {
        "token": token,
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "is_admin": user.get("is_admin", False),
            "is_member": user.get("is_member", False)
        }
    }

@api_router.get("/auth/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {
        "id": user["id"],
        "email": user["email"],
        "name": user["name"],
        "is_admin": user.get("is_admin", False),
        "is_member": user.get("is_member", False),
        "chat_count": user.get("chat_count", 0)
    }

@api_router.post("/chat/send", response_model=ChatResponse)
async def send_chat(request: ChatRequest):
    # Chat endpoint works for both authenticated and guest users
    user = None
    
    session_id = request.session_id or str(uuid.uuid4())
    
    # Search for drug in query
    drug_info = search_drug(request.message)
    
    if not drug_info and any(keyword in request.message.lower() for keyword in ['drug', 'medicine', 'medication', 'tablet', 'capsule']):
        return ChatResponse(
            response="Out of my context 😊\n\nI can only provide information about medications in my verified pharmacopoeia database. Currently, I have information about: Aspirin, Paracetamol, Amoxicillin, and Ibuprofen.\n\n⚠️ This is for educational purposes only. Please consult a qualified healthcare professional.",
            session_id=session_id,
            citations=None,
            drug_info=None
        )
    
    # Get AI response
    ai_response, citations = get_ai_response(request.message, drug_info)
    
    # Skip database storage for now (MongoDB not available)
    # In production, uncomment the database save lines below:
    # message_doc = {
    #     "id": str(uuid.uuid4()),
    #     "session_id": session_id,
    #     "user_message": request.message,
    #     "ai_response": ai_response,
    #     "citations": citations,
    #     "drug_info": drug_info,
    #     "timestamp": datetime.now(timezone.utc).isoformat()
    # }
    # await db.chat_messages.insert_one(message_doc)
    
    return ChatResponse(
        response=ai_response,
        session_id=session_id,
        citations=citations,
        drug_info=drug_info
    )

@api_router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    messages = await db.chat_messages.find({"session_id": session_id}, {"_id": 0}).sort("timestamp", 1).to_list(100)
    return messages

@api_router.get("/chat/sessions")
async def get_user_sessions(user: dict = Depends(get_current_user)):
    # Get last 5 unique sessions
    pipeline = [
        {"$sort": {"timestamp": -1}},
        {"$group": {
            "_id": "$session_id",
            "last_message": {"$first": "$user_message"},
            "timestamp": {"$first": "$timestamp"}
        }},
        {"$sort": {"timestamp": -1}},
        {"$limit": 5}
    ]
    
    sessions = await db.chat_messages.aggregate(pipeline).to_list(5)
    return [{"session_id": s["_id"], "last_message": s["last_message"], "timestamp": s["timestamp"]} for s in sessions]

@api_router.post("/feedback/submit")
async def submit_feedback(feedback: FeedbackSubmit, user: Optional[dict] = None):
    feedback_doc = {
        "id": str(uuid.uuid4()),
        "session_id": feedback.session_id,
        "message_id": feedback.message_id,
        "rating": feedback.rating,
        "message_content": feedback.message_content,
        "response_content": feedback.response_content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_email": user["email"] if user else "anonymous"
    }
    
    await db.feedback.insert_one(feedback_doc)
    return {"message": "Feedback submitted successfully"}

@api_router.get("/feedback/all", response_model=List[Feedback])
async def get_all_feedback(admin: dict = Depends(get_admin_user)):
    feedback_list = await db.feedback.find({}, {"_id": 0}).sort("timestamp", -1).to_list(1000)
    return feedback_list

@api_router.get("/")
async def root():
    return {"message": "Medcures API is running"}

app.include_router(api_router)

# Production-safe CORS configuration
cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
cors_origins = [origin.strip() for origin in cors_origins]  # Remove whitespace

# In production, only allow specific origins
if IS_PRODUCTION and '*' in cors_origins:
    logger.error("❌ CORS_ORIGINS=* is NOT allowed in production!")
    logger.error("   Please set specific domains in .env: CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com")
    raise ValueError("Wildcard CORS origins not allowed in production")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Security Headers Middleware for production
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    
    # Security headers - critical for production
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains" if IS_PRODUCTION else ""
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ===== HEALTH CHECK ENDPOINT (for 24/7 reliability) =====
@app.get("/health")
async def health_check():
    """Simple health check endpoint - returns OK if server is running"""
    return {
        "status": "ok",
        "environment": ENVIRONMENT,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.on_event("shutdown")
async def shutdown_db_client():
    if 'client' in globals() and client:
        client.close()