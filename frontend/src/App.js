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

  if (page === 'landing') {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#0B0F17', color: 'white', fontFamily: 'Arial, sans-serif' }}>
        <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '20px 50px' }}>
          <div></div>
          <div style={{ display: 'flex', gap: '15px' }}>
            <button onClick={() => setPage('login')} style={{ padding: '10px 20px', background: 'none', border: 'none', color: 'white', cursor: 'pointer', fontSize: '16px' }}>Login</button>
            <button onClick={() => setPage('signup')} style={{ padding: '10px 30px', background: '#38BDF8', color: '#0B0F17', border: 'none', borderRadius: '20px', cursor: 'pointer', fontSize: '16px', fontWeight: 'bold' }}>Sign Up</button>
          </div>
        </header>

        <main style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: 'calc(100vh - 80px)', textAlign: 'center', padding: '30px' }}>
          <h1 style={{ fontSize: '56px', marginBottom: '20px', lineHeight: '1.2' }}>
            Your Trusted Medical Information<br /><span style={{ color: '#38BDF8' }}>Companion</span>
          </h1>
          <p style={{ fontSize: '18px', color: '#999', marginBottom: '40px', maxWidth: '600px' }}>
            Get verified pharmaceutical information from trusted sources.
          </p>

          <div style={{ width: '100%', maxWidth: '600px', marginBottom: '50px' }}>
            <input
              type="text"
              placeholder="Ask about any medication... (e.g., Aspirin)"
              onKeyPress={(e) => {
                if (e.key === 'Enter' && e.target.value.trim()) {
                  setInput(e.target.value);
                  setPage('chat');
                }
              }}
              style={{ width: '100%', padding: '15px', fontSize: '16px', borderRadius: '30px', border: 'none', backgroundColor: 'white', color: '#333' }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', maxWidth: '1000px', width: '100%' }}>
            <div style={{ padding: '20px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '15px' }}>
              <h3 style={{ marginBottom: '10px' }}>Verified Sources</h3>
              <p style={{ fontSize: '14px', color: '#999' }}>Trusted database information</p>
            </div>
            <div style={{ padding: '20px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '15px' }}>
              <h3 style={{ marginBottom: '10px' }}>Educational</h3>
              <p style={{ fontSize: '14px', color: '#999' }}>Professional medical data</p>
            </div>
            <div style={{ padding: '20px', background: 'rgba(255, 255, 255, 0.05)', borderRadius: '15px' }}>
              <h3 style={{ marginBottom: '10px' }}>AI-Powered</h3>
              <p style={{ fontSize: '14px', color: '#999' }}>Advanced analysis</p>
            </div>
          </div>
        </main>
      </div>
    );
  }

  if (page === 'chat') {
    return (
      <div style={{ minHeight: '100vh', backgroundColor: '#0B0F17', color: 'white', fontFamily: 'Arial, sans-serif', display: 'flex', flexDirection: 'column' }}>
        <header style={{ padding: '20px 50px', borderBottom: '1px solid rgba(255, 255, 255, 0.1)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <button onClick={() => setPage('landing')} style={{ background: 'none', border: 'none', color: '#38BDF8', cursor: 'pointer', fontSize: '16px' }}>← Back</button>
          <h1>Chat</h1>
          <div></div>
        </header>

        <div style={{ flex: '1', overflowY: 'auto', padding: '30px 50px' }}>
          {messages.length === 0 && <p style={{ textAlign: 'center', color: '#999' }}>Ask about any medication...</p>}
          {messages.map((msg, i) => (
            <div key={i} style={{ marginBottom: '15px', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
              <div style={{
                display: 'inline-block',
                maxWidth: '70%',
                padding: '12px 18px',
                borderRadius: '12px',
                backgroundColor: msg.role === 'user' ? '#38BDF8' : 'rgba(255, 255, 255, 0.1)',
                color: msg.role === 'user' ? '#0B0F17' : 'white'
              }}>
                {msg.content}
              </div>
            </div>
          ))}
        </div>

        <div style={{ padding: '20px 50px', borderTop: '1px solid rgba(255, 255, 255, 0.1)', display: 'flex', gap: '10px', maxWidth: '900px', margin: '0 auto', width: '100%' }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Ask about medication..."
            style={{ flex: '1', padding: '12px', borderRadius: '8px', border: '1px solid rgba(255, 255, 255, 0.2)', backgroundColor: 'rgba(255, 255, 255, 0.05)', color: 'white', fontSize: '14px' }}
          />
          <button
            onClick={sendMessage}
            style={{ padding: '12px 25px', background: '#38BDF8', color: '#0B0F17', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}
          >
            Send
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0B0F17', color: 'white', fontFamily: 'Arial, sans-serif', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ textAlign: 'center' }}>
        <h1>{page.charAt(0).toUpperCase() + page.slice(1)}</h1>
        <button onClick={() => setPage('landing')} style={{ marginTop: '20px', padding: '10px 30px', background: 'white', color: '#0B0F17', border: 'none', borderRadius: '8px', cursor: 'pointer', fontWeight: 'bold' }}>Back Home</button>
      </div>
    </div>
  );
}

export default App;