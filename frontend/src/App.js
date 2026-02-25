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
        {/* Background Image */}
        <div style={{
          position: 'absolute',
          inset: 0,
          opacity: 0.1,
          backgroundImage: 'url(https://images.unsplash.com/photo-1607893326676-5c46ba36251f?crop=entropy&cs=srgb&fm=jpg&q=85)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}></div>

        <div style={{ position: 'relative', zIndex: 10 }}>
          <header style={{ padding: '20px 40px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
            <button
              onClick={() => setPage('landing')}
              style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '8px', transition: 'color 0.3s' }}
              onMouseEnter={(e) => e.target.style.color = '#38BDF8'}
              onMouseLeave={(e) => e.target.style.color = '#cbd5e1'}
            >
              ⬅ Back to Home
            </button>
          </header>

          <div style={{ maxHeight: 'calc(100vh - 100px)', overflowY: 'auto', padding: '40px 20px' }}>
            <div style={{ maxWidth: '900px', margin: '0 auto', color: 'white' }}>
              <h1 style={{ fontSize: '36px', fontWeight: '400', marginBottom: '12px' }}>Privacy Policy</h1>
              <p style={{ color: '#94a3b8', marginBottom: '40px', fontSize: '14px' }}>Last updated: January 2026</p>

              {/* Section 1 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>1. Information We Collect</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '12px' }}>
                  We collect information that you provide directly to us, including:
                </p>
                <ul style={{ listStyle: 'disc', marginLeft: '24px', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <li>Account information (email, name, password)</li>
                  <li>Chat messages and queries</li>
                  <li>Feedback and ratings</li>
                  <li>Usage data and preferences</li>
                </ul>
              </section>

              {/* Section 2 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>2. How We Use Your Information</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '12px' }}>
                  We use the information we collect to:
                </p>
                <ul style={{ listStyle: 'disc', marginLeft: '24px', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <li>Provide and improve our services</li>
                  <li>Respond to your queries with relevant medical information</li>
                  <li>Send important updates and notifications</li>
                  <li>Analyze usage patterns to enhance user experience</li>
                </ul>
              </section>

              {/* Section 3 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>3. Data Storage and Security</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '12px' }}>
                  We implement appropriate security measures to protect your personal information:
                </p>
                <ul style={{ listStyle: 'disc', marginLeft: '24px', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <li>Encrypted storage of chat history (last 5 chats per user)</li>
                  <li>Secure password hashing</li>
                  <li>Regular security audits</li>
                  <li>Limited data retention policies</li>
                </ul>
              </section>

              {/* Section 4 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>4. Data Sharing</h2>
                <p style={{ color: '#cbd5e1' }}>
                  We do NOT sell, trade, or rent your personal information to third parties. Feedback data is accessible only to authorized administrators for quality improvement purposes.
                </p>
              </section>

              {/* Section 5 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>5. Your Rights (GDPR Compliance)</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '12px' }}>
                  You have the right to:
                </p>
                <ul style={{ listStyle: 'disc', marginLeft: '24px', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <li>Access your personal data</li>
                  <li>Request correction of inaccurate data</li>
                  <li>Request deletion of your account and data</li>
                  <li>Object to data processing</li>
                  <li>Data portability</li>
                </ul>
              </section>

              {/* Section 6 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>6. Medical Information Disclaimer</h2>
                <p style={{ color: '#cbd5e1' }}>
                  We do NOT store personal health information. All information provided is for educational purposes only. We are not responsible for any medical decisions made based on information from our platform.
                </p>
              </section>

              {/* Section 7 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>7. Contact Us</h2>
                <p style={{ color: '#cbd5e1' }}>
                  For privacy-related questions or to exercise your rights, contact us at: <strong>medcures15@gmail.com</strong>
                </p>
              </section>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (page === 'terms') {
    return (
      <div style={bgStyle}>
        {/* Background Image */}
        <div style={{
          position: 'absolute',
          inset: 0,
          opacity: 0.1,
          backgroundImage: 'url(https://images.unsplash.com/photo-1607893326676-5c46ba36251f?crop=entropy&cs=srgb&fm=jpg&q=85)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}></div>

        <div style={{ position: 'relative', zIndex: 10 }}>
          <header style={{ padding: '20px 40px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)' }}>
            <button
              onClick={() => setPage('landing')}
              style={{ background: 'none', border: 'none', color: '#cbd5e1', cursor: 'pointer', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '8px', transition: 'color 0.3s' }}
              onMouseEnter={(e) => e.target.style.color = '#38BDF8'}
              onMouseLeave={(e) => e.target.style.color = '#cbd5e1'}
            >
              ⬅ Back to Home
            </button>
          </header>

          <div style={{ maxHeight: 'calc(100vh - 100px)', overflowY: 'auto', padding: '40px 20px' }}>
            <div style={{ maxWidth: '900px', margin: '0 auto', color: 'white' }}>
              <h1 style={{ fontSize: '36px', fontWeight: '400', marginBottom: '12px' }}>Terms & Conditions</h1>
              <p style={{ color: '#94a3b8', marginBottom: '40px', fontSize: '14px' }}>Last updated: January 2026</p>

              {/* Section 1 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>1. Acceptance of Terms</h2>
                <p style={{ color: '#cbd5e1' }}>
                  By accessing and using Medcures, you accept and agree to be bound by these Terms and Conditions. If you do not agree, please discontinue use immediately.
                </p>
              </section>

              {/* Section 2 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>2. Educational Purpose Only</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '12px' }}>
                  Medcures provides pharmaceutical information for <strong>EDUCATIONAL PURPOSES ONLY</strong>. This platform:
                </p>
                <ul style={{ listStyle: 'disc', marginLeft: '24px', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <li>Does NOT provide medical advice, diagnosis, or treatment</li>
                  <li>Does NOT replace professional medical consultation</li>
                  <li>Should NOT be used for self-diagnosis or self-medication</li>
                  <li>Is NOT a substitute for licensed healthcare professionals</li>
                </ul>
              </section>

              {/* Section 3 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>3. Medical Disclaimer</h2>
                <p style={{ color: '#FF6B6B', fontWeight: 'bold', marginBottom: '12px' }}>
                  ⚠️ <strong>IMPORTANT:</strong> Always consult with a qualified healthcare professional before taking any medication or making health-related decisions. Individual medical conditions vary, and professional evaluation is essential.
                </p>
              </section>

              {/* Section 4 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>4. User Responsibilities</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '12px' }}>
                  You agree to:
                </p>
                <ul style={{ listStyle: 'disc', marginLeft: '24px', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <li>Use the platform responsibly and ethically</li>
                  <li>Not share false or misleading information</li>
                  <li>Maintain confidentiality of your account credentials</li>
                  <li>Not attempt to compromise platform security</li>
                  <li>Respect intellectual property rights</li>
                </ul>
              </section>

              {/* Section 5 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>5. Usage Limits</h2>
                <p style={{ color: '#cbd5e1' }}>
                  Guest users are limited to 3 chat interactions. Registered users have extended access. Premium membership may be required for unlimited usage.
                </p>
              </section>

              {/* Section 6 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>6. Information Accuracy</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '12px' }}>
                  While we strive to provide accurate information from verified pharmacopoeia sources (British Pharmacopoeia, USP, FDA), we cannot guarantee:
                </p>
                <ul style={{ listStyle: 'disc', marginLeft: '24px', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <li>100% accuracy or completeness of information</li>
                  <li>Real-time updates for all medications</li>
                  <li>Suitability for specific individual cases</li>
                </ul>
              </section>

              {/* Section 7 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>7. Limitation of Liability</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '12px' }}>
                  Medcures and its founders are NOT liable for:
                </p>
                <ul style={{ listStyle: 'disc', marginLeft: '24px', color: '#cbd5e1', lineHeight: '1.8' }}>
                  <li>Any medical decisions made based on platform information</li>
                  <li>Adverse effects from medication use</li>
                  <li>Errors or omissions in information provided</li>
                  <li>Damages resulting from platform use or inability to use</li>
                </ul>
              </section>

              {/* Section 8 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>8. Intellectual Property</h2>
                <p style={{ color: '#cbd5e1' }}>
                  All content, design, and technology on Medcures are protected by intellectual property laws. Unauthorized reproduction or distribution is prohibited.
                </p>
              </section>

              {/* Section 9 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>9. Modifications</h2>
                <p style={{ color: '#cbd5e1' }}>
                  We reserve the right to modify these terms at any time. Continued use after changes constitutes acceptance of modified terms.
                </p>
              </section>

              {/* Section 10 */}
              <section style={{ marginBottom: '40px', lineHeight: '1.8' }}>
                <h2 style={{ fontSize: '22px', fontWeight: '500', color: '#38BDF8', marginBottom: '16px' }}>10. Contact Information</h2>
                <p style={{ color: '#cbd5e1', marginBottom: '20px' }}>
                  For questions or concerns about these terms, contact us at: <strong>medcures15@gmail.com</strong>
                </p>
                <p style={{ color: '#94a3b8', fontSize: '14px', lineHeight: '1.6' }}>
                  <strong>Founders:</strong> Zainab Bohra & Shriya Soni<br />
                  <strong>Sponsored by:</strong> U.S Ostwal Institute of Pharmacy<br />
                  <strong>Co-founder:</strong> Ishika Chourdiya
                </p>
              </section>
            </div>
          </div>
        </div>
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