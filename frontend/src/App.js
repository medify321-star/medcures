import React, { useState } from 'react';
import './App.css';

function App() {
  const [page, setPage] = useState('landing');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId] = useState('guest-' + Date.now());

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const userMsg = input;
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setInput('');
    
    try {
      const res = await fetch('http://localhost:8000/api/chat/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg, session_id: sessionId })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Could not reach backend' }]);
    }
  };

  const bgStyle = {
    minHeight: '100vh',
    backgroundColor: '#0B0F17',
    color: 'white',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    position: 'relative',
    overflow: 'hidden'
  };

  if (page === 'landing') {
    return (
      <div style={bgStyle}>
        {/* Background Image */}
        <div style={{
          position: 'absolute',
          inset: 0,
          opacity: 0.3,
          backgroundImage: 'url(https://images.unsplash.com/photo-1607893326676-5c46ba36251f?crop=entropy&cs=srgb&fm=jpg&q=85)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}></div>

        {/* Gradient Overlay */}
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.15) 0%, rgba(11, 15, 23, 0) 70%)'
        }}></div>

        {/* Content */}
        <div style={{ position: 'relative', zIndex: 10 }}>
          {/* Header */}
          <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px 50px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
            <div style={{ fontSize: '28px', fontWeight: '600', letterSpacing: '-0.5px', background: 'linear-gradient(135deg, #38BDF8, #2DD4BF)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>Medcures</div>
            <div style={{ display: 'flex', gap: '15px' }}>
              <button 
                onClick={() => setPage('login')} 
                style={{ 
                  padding: '10px 20px', 
                  background: 'none', 
                  border: 'none', 
                  color: '#b0b0b0', 
                  cursor: 'pointer', 
                  fontSize: '15px',
                  transition: 'color 0.3s'
                }}
                onMouseEnter={(e) => e.target.style.color = 'white'}
                onMouseLeave={(e) => e.target.style.color = '#b0b0b0'}
              >
                Login
              </button>
              <button 
                onClick={() => setPage('signup')} 
                style={{ 
                  padding: '10px 24px', 
                  background: '#38BDF8', 
                  color: '#0B0F17', 
                  border: 'none', 
                  borderRadius: '20px', 
                  cursor: 'pointer', 
                  fontSize: '15px', 
                  fontWeight: '600',
                  boxShadow: '0 0 20px rgba(56, 189, 248, 0.3)',
                  transition: 'all 0.3s'
                }}
                onMouseEnter={(e) => {
                  e.target.style.background = '#0EA5E9';
                  e.target.style.boxShadow = '0 0 30px rgba(56, 189, 248, 0.5)';
                }}
                onMouseLeave={(e) => {
                  e.target.style.background = '#38BDF8';
                  e.target.style.boxShadow = '0 0 20px rgba(56, 189, 248, 0.3)';
                }}
              >
                Sign Up
              </button>
            </div>
          </header>

          {/* Main Content */}
          <main style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: 'calc(100vh - 200px)', textAlign: 'center', padding: '40px 30px', maxWidth: '1200px', margin: '0 auto' }}>
            <h1 style={{ fontSize: '60px', lineHeight: '1.2', fontWeight: '400', letterSpacing: '-1px', marginBottom: '25px', maxWidth: '900px' }}>
              Your Trusted Medical Information
              <br />
              <span style={{ color: '#38BDF8', fontWeight: '500' }}>Companion</span>
            </h1>
            
            <p style={{ fontSize: '18px', color: '#94a3b8', marginBottom: '45px', maxWidth: '700px', lineHeight: '1.6' }}>
              Get verified pharmaceutical information from trusted sources. Educational guidance for informed healthcare decisions.
            </p>

            {/* Search Bar with Icon */}
            <div style={{ width: '100%', maxWidth: '650px', marginBottom: '60px' }}>
              <div style={{ position: 'relative' }}>
                <span style={{ position: 'absolute', left: '20px', top: '50%', transform: 'translateY(-50%)', fontSize: '18px' }}>🔍</span>
                <input
                  type="text"
                  placeholder="Ask about any medication... (e.g., Aspirin, Paracetamol)"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && e.target.value.trim()) {
                      setInput(e.target.value);
                      setPage('chat');
                    }
                  }}
                  style={{ 
                    width: '100%', 
                    padding: '16px 20px 16px 50px', 
                    fontSize: '16px', 
                    borderRadius: '34px', 
                    border: 'none', 
                    backgroundColor: '#F1F5F9', 
                    color: '#1e293b',
                    boxShadow: '0 8px 24px rgba(0, 0, 0, 0.3)',
                    outline: 'none'
                  }}
                  onFocus={(e) => {
                    e.target.style.boxShadow = '0 8px 32px rgba(56, 189, 248, 0.4)';
                    e.target.style.borderColor = '#38BDF8';
                  }}
                  onBlur={(e) => {
                    e.target.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.3)';
                  }}
                />
              </div>
            </div>

            {/* Feature Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '25px', maxWidth: '1100px', width: '100%', marginTop: '20px' }}>
              <div 
                style={{ 
                  padding: '30px', 
                  background: 'rgba(255, 255, 255, 0.08)', 
                  borderRadius: '20px', 
                  backdropFilter: 'blur(12px)',
                  border: '1px solid rgba(56, 189, 248, 0.3)',
                  transition: 'all 0.3s',
                  textAlign: 'left'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.12)';
                  e.currentTarget.style.borderColor = 'rgba(56, 189, 248, 0.5)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)';
                  e.currentTarget.style.borderColor = 'rgba(56, 189, 248, 0.3)';
                }}
              >
                <div style={{ fontSize: '28px', marginBottom: '12px' }}>🛡️</div>
                <h3 style={{ marginBottom: '12px', color: '#38BDF8', fontSize: '18px', fontWeight: '600' }}>Verified Sources</h3>
                <p style={{ fontSize: '14px', color: '#cbd5e1', lineHeight: '1.6' }}>Information from British Pharmacopoeia, USP, and FDA databases</p>
              </div>

              <div 
                style={{ 
                  padding: '30px', 
                  background: 'rgba(255, 255, 255, 0.08)', 
                  borderRadius: '20px', 
                  backdropFilter: 'blur(12px)',
                  border: '1px solid rgba(45, 212, 191, 0.3)',
                  transition: 'all 0.3s',
                  textAlign: 'left'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.12)';
                  e.currentTarget.style.borderColor = 'rgba(45, 212, 191, 0.5)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)';
                  e.currentTarget.style.borderColor = 'rgba(45, 212, 191, 0.3)';
                }}
              >
                <div style={{ fontSize: '28px', marginBottom: '12px' }}>📚</div>
                <h3 style={{ marginBottom: '12px', color: '#2DD4BF', fontSize: '18px', fontWeight: '600' }}>Educational Purpose</h3>
                <p style={{ fontSize: '14px', color: '#cbd5e1', lineHeight: '1.6' }}>Professional medical information for learning and reference</p>
              </div>

              <div 
                style={{ 
                  padding: '30px', 
                  background: 'rgba(255, 255, 255, 0.08)', 
                  borderRadius: '20px', 
                  backdropFilter: 'blur(12px)',
                  border: '1px solid rgba(99, 102, 241, 0.3)',
                  transition: 'all 0.3s',
                  textAlign: 'left'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.12)';
                  e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.5)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = 'rgba(255, 255, 255, 0.08)';
                  e.currentTarget.style.borderColor = 'rgba(99, 102, 241, 0.3)';
                }}
              >
                <div style={{ fontSize: '28px', marginBottom: '12px' }}>✨</div>
                <h3 style={{ marginBottom: '12px', color: '#6366F1', fontSize: '18px', fontWeight: '600' }}>AI-Powered</h3>
                <p style={{ fontSize: '14px', color: '#cbd5e1', lineHeight: '1.6' }}>Smart responses with proper citations and disclaimers</p>
              </div>
            </div>
          </main>

          {/* Footer */}
          <footer style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            gap: '30px', 
            padding: '30px 20px', 
            borderTop: '1px solid rgba(255, 255, 255, 0.05)', 
            color: '#64748b', 
            fontSize: '14px',
            flexWrap: 'wrap'
          }}>
            <button 
              onClick={() => setPage('privacy')} 
              style={{ 
                background: 'none', 
                border: 'none', 
                color: '#64748b', 
                cursor: 'pointer',
                transition: 'color 0.3s'
              }}
              onMouseEnter={(e) => e.target.style.color = '#38BDF8'}
              onMouseLeave={(e) => e.target.style.color = '#64748b'}
            >
              Privacy Policy
            </button>
            <span>·</span>
            <button 
              onClick={() => setPage('terms')} 
              style={{ 
                background: 'none', 
                border: 'none', 
                color: '#64748b', 
                cursor: 'pointer',
                transition: 'color 0.3s'
              }}
              onMouseEnter={(e) => e.target.style.color = '#38BDF8'}
              onMouseLeave={(e) => e.target.style.color = '#64748b'}
            >
              Terms & Conditions
            </button>
            <span>·</span>
            <button 
              onClick={() => setPage('disclaimer')} 
              style={{ 
                background: 'none', 
                border: 'none', 
                color: '#64748b', 
                cursor: 'pointer',
                transition: 'color 0.3s'
              }}
              onMouseEnter={(e) => e.target.style.color = '#38BDF8'}
              onMouseLeave={(e) => e.target.style.color = '#64748b'}
            >
              Disclaimer
            </button>
          </footer>
        </div>
      </div>
    );
  }

  if (page === 'chat') {
    return (
      <div style={{ ...bgStyle, display: 'flex', flexDirection: 'column' }}>
        <header style={{ padding: '20px 40px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(11, 15, 23, 0.8)', backdropFilter: 'blur(6px)' }}>
          <button 
            onClick={() => setPage('landing')} 
            style={{ background: 'none', border: 'none', color: '#38BDF8', cursor: 'pointer', fontSize: '16px', fontWeight: '500' }}
          >
            ← Back to Home
          </button>
          <h2 style={{ color: '#38BDF8', fontSize: '18px', fontWeight: '600' }}>Medical Information Chat</h2>
          <div></div>
        </header>

        <div style={{ flex: '1', overflowY: 'auto', padding: '30px 40px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', color: '#64748b', marginTop: '60px', fontSize: '16px' }}>
              <p style={{ fontSize: '24px', marginBottom: '10px' }}>💬</p>
              <p>Ask about any medication...</p>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
              <div style={{
                maxWidth: '65%',
                padding: '14px 18px',
                borderRadius: '16px',
                backgroundColor: msg.role === 'user' ? '#38BDF8' : 'rgba(255, 255, 255, 0.1)',
                color: msg.role === 'user' ? '#0B0F17' : '#e2e8f0',
                lineHeight: '1.5',
                wordWrap: 'break-word',
                backdropFilter: msg.role === 'assistant' ? 'blur(4px)' : 'none'
              }}>
                {msg.content}
              </div>
            </div>
          ))}
        </div>

        <div style={{ padding: '20px 40px', borderTop: '1px solid rgba(255, 255, 255, 0.1)', background: 'rgba(11, 15, 23, 0.9)', backdropFilter: 'blur(6px)' }}>
          <div style={{ display: 'flex', gap: '12px', maxWidth: '1000px', margin: '0 auto' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask about medication..."
              style={{ 
                flex: '1', 
                padding: '12px 16px', 
                borderRadius: '20px', 
                border: '1px solid rgba(56, 189, 248, 0.3)',
                backgroundColor: 'rgba(255, 255, 255, 0.05)', 
                color: 'white', 
                fontSize: '14px',
                outline: 'none'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = 'rgba(56, 189, 248, 0.6)';
                e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.08)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = 'rgba(56, 189, 248, 0.3)';
                e.target.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
              }}
            />
            <button
              onClick={sendMessage}
              style={{ 
                padding: '12px 28px', 
                background: '#38BDF8', 
                color: '#0B0F17', 
                border: 'none', 
                borderRadius: '20px', 
                cursor: 'pointer', 
                fontWeight: '600',
                transition: 'all 0.3s',
                boxShadow: '0 0 16px rgba(56, 189, 248, 0.2)'
              }}
              onMouseEnter={(e) => {
                e.target.style.background = '#0EA5E9';
                e.target.style.boxShadow = '0 0 24px rgba(56, 189, 248, 0.4)';
              }}
              onMouseLeave={(e) => {
                e.target.style.background = '#38BDF8';
                e.target.style.boxShadow = '0 0 16px rgba(56, 189, 248, 0.2)';
              }}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (page === 'privacy') {
    return (
      <div style={bgStyle}>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px 50px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
          <button onClick={() => setPage('landing')} style={{ background: 'none', border: 'none', color: '#38BDF8', cursor: 'pointer', fontSize: '16px' }}>← Back</button>
          <h1>Privacy Policy</h1>
          <div></div>
        </header>
        <main style={{ maxWidth: '800px', margin: '0 auto', padding: '40px', lineHeight: '1.8', color: '#ccc' }}>
          <h2 style={{ color: '#38BDF8', marginBottom: '20px' }}>Privacy Policy</h2>
          <p>At Medcures, we respect your privacy and are committed to protecting your personal data. This Privacy Policy explains how we collect, use, and protect information when you use our platform.</p>
          
          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Information We Collect</h3>
          <p>We collect information you provide directly, such as email address and usage data. We also collect information about how you interact with our service.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>How We Use Your Information</h3>
          <p>We use your information to provide and improve our services, communicate with you, and comply with legal obligations.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Data Security</h3>
          <p>We implement appropriate technical and organizational measures to protect your personal data against unauthorized access, alteration, disclosure, or destruction.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Contact Us</h3>
          <p>If you have questions about this Privacy Policy, please contact us at privacy@medcures.com</p>
        </main>
      </div>
    );
  }

  if (page === 'terms') {
    return (
      <div style={bgStyle}>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px 50px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
          <button onClick={() => setPage('landing')} style={{ background: 'none', border: 'none', color: '#38BDF8', cursor: 'pointer', fontSize: '16px' }}>← Back</button>
          <h1>Terms & Conditions</h1>
          <div></div>
        </header>
        <main style={{ maxWidth: '800px', margin: '0 auto', padding: '40px', lineHeight: '1.8', color: '#ccc' }}>
          <h2 style={{ color: '#38BDF8', marginBottom: '20px' }}>Terms & Conditions</h2>
          <p>Welcome to Medcures. These terms and conditions govern your use of our platform and services.</p>
          
          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Use License</h3>
          <p>Permission is granted to temporarily download one copy of the materials (information or software) on Medcures for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Disclaimer</h3>
          <p>The materials on Medcures are provided on an 'as is' basis. Medcures makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including, without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Limitations</h3>
          <p>In no event shall Medcures or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on Medcures.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Modifications</h3>
          <p>Medcures may revise these terms and conditions for its website at any time without notice. By using this website, you are agreeing to be bound by the then current version of these terms and conditions.</p>
        </main>
      </div>
    );
  }

  if (page === 'disclaimer') {
    return (
      <div style={bgStyle}>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px 50px', borderBottom: '1px solid rgba(255, 255, 255, 0.05)' }}>
          <button onClick={() => setPage('landing')} style={{ background: 'none', border: 'none', color: '#38BDF8', cursor: 'pointer', fontSize: '16px' }}>← Back</button>
          <h1>Medical Disclaimer</h1>
          <div></div>
        </header>
        <main style={{ maxWidth: '800px', margin: '0 auto', padding: '40px', lineHeight: '1.8', color: '#ccc' }}>
          <h2 style={{ color: '#38BDF8', marginBottom: '20px' }}>Medical Disclaimer</h2>
          <p style={{ fontSize: '16px', fontWeight: 'bold', color: '#FF6B6B' }}>⚠️ IMPORTANT: PLEASE READ CAREFULLY</p>
          
          <p style={{ marginTop: '20px' }}>The information provided on Medcures is for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>No Medical Advice</h3>
          <p>Nothing on this website constitutes professional medical advice. Always consult with a qualified medical professional before making any healthcare decisions.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Educational Purpose Only</h3>
          <p>Medcures provides information about medications for educational purposes only. This information is not intended to diagnose, treat, cure, or prevent any disease.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Accuracy</h3>
          <p>While we strive to provide accurate and up-to-date information, we do not guarantee the accuracy, completeness, or timeliness of any information on our platform.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Liability</h3>
          <p>Medcures shall not be liable for any damage or loss arising from your use of or reliance upon information provided on our platform.</p>

          <h3 style={{ color: '#38BDF8', marginTop: '30px', marginBottom: '15px' }}>Medical Emergency</h3>
          <p>If you are experiencing a medical emergency, please contact emergency services or visit your nearest hospital immediately.</p>
        </main>
      </div>
    );
  }

  if (page === 'login') {
    return (
      <div style={{ ...bgStyle, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '100%', maxWidth: '400px', padding: '40px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '15px', border: '1px solid rgba(56, 189, 248, 0.3)' }}>
          <h1 style={{ textAlign: 'center', marginBottom: '30px', color: '#38BDF8' }}>Login</h1>
          <p style={{ textAlign: 'center', color: '#aaa', marginBottom: '20px' }}>Coming Soon</p>
          <button 
            onClick={() => setPage('landing')}
            style={{ width: '100%', padding: '12px', background: '#38BDF8', color: '#0B0F17', fontWeight: 'bold', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  if (page === 'signup') {
    return (
      <div style={{ ...bgStyle, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '100%', maxWidth: '400px', padding: '40px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '15px', border: '1px solid rgba(56, 189, 248, 0.3)' }}>
          <h1 style={{ textAlign: 'center', marginBottom: '30px', color: '#38BDF8' }}>Sign Up</h1>
          <p style={{ textAlign: 'center', color: '#aaa', marginBottom: '20px' }}>Coming Soon</p>
          <button 
            onClick={() => setPage('landing')}
            style={{ width: '100%', padding: '12px', background: '#38BDF8', color: '#0B0F17', fontWeight: 'bold', border: 'none', borderRadius: '8px', cursor: 'pointer' }}
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return null;
}

export default App;