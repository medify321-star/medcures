import React, { useState } from 'react';
import './App.css';

function App() {
  const [page, setPage] = useState('landing');
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId] = useState('guest-' + Date.now());
  const [token, setToken] = useState(localStorage.getItem('medcures_token'));

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    setMessages([...messages, { role: 'user', content: input }]);
    
    try {
      const response = await fetch('http://localhost:8000/api/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token && { 'Authorization': `Bearer ${token}` })
        },
        body: JSON.stringify({
          message: input,
          session_id: sessionId
        })
      });
      
      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, there was an error. Please try again.' }]);
    }
    
    setInput('');
  };

  return (
    <div className="min-h-screen bg-[#0B0F17] text-white">
      {page === 'landing' && (
        <div className="min-h-screen flex flex-col">
          {/* Header */}
          <header className="flex justify-between items-center px-12 py-6">
            <div></div>
            <div className="flex gap-3">
              <button 
                onClick={() => setPage('login')}
                className="px-6 py-2 hover:bg-white/10 rounded-lg transition"
              >
                Login
              </button>
              <button 
                onClick={() => setPage('signup')}
                className="px-6 py-2 bg-[#38BDF8] text-[#0B0F17] rounded-full hover:bg-[#0EA5E9] transition"
              >
                Sign Up
              </button>
            </div>
          </header>

          {/* Hero */}
          <main className="flex-1 flex flex-col items-center justify-center px-12 text-center">
            <h1 className="text-6xl font-bold text-white mb-4">
              Your Trusted Medical Information
              <span className="block text-[#38BDF8] mt-2">Companion</span>
            </h1>
            <p className="text-xl text-gray-300 mb-12 max-w-2xl">
              Get verified pharmaceutical information from trusted sources. Educational guidance for informed healthcare decisions.
            </p>
            
            {/* Search */}
            <div className="w-full max-w-3xl mb-16">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Ask about any medication... (e.g., Aspirin, Paracetamol)"
                  className="w-full h-14 pl-6 pr-6 text-lg bg-white text-gray-900 rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-[#38BDF8]"
                  onKeyPress={(e) => e.key === 'Enter' && (setInput(e.target.value), setPage('chat'))}
                />
              </div>
            </div>

            {/* Features */}
            <div className="grid grid-cols-3 gap-6 max-w-4xl">
              <div className="p-6 bg-white/5 rounded-2xl text-left">
                <h3 className="text-xl font-semibold mb-2">Verified Sources</h3>
                <p className="text-gray-400">Information from trusted databases</p>
              </div>
              <div className="p-6 bg-white/5 rounded-2xl text-left">
                <h3 className="text-xl font-semibold mb-2">Educational</h3>
                <p className="text-gray-400">Professional medical information</p>
              </div>
              <div className="p-6 bg-white/5 rounded-2xl text-left">
                <h3 className="text-xl font-semibold mb-2">AI-Powered</h3>
                <p className="text-gray-400">Advanced analysis and insights</p>
              </div>
            </div>
          </main>
        </div>
      )}

      {page === 'chat' && (
        <div className="min-h-screen flex flex-col">
          {/* Header */}
          <header className="flex justify-between items-center px-12 py-6 border-b border-white/10">
            <button 
              onClick={() => setPage('landing')}
              className="text-[#38BDF8] hover:text-white"
            >
              ← Back
            </button>
            <h1 className="text-2xl font-bold">Chat</h1>
            <div></div>
          </header>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto px-12 py-6">
            {messages.length === 0 && (
              <div className="text-center text-gray-400 py-12">
                <p>Welcome to Medcures Chat!</p>
                <p>Ask about any medication...</p>
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`mb-6 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                <div className={`inline-block max-w-2xl px-6 py-3 rounded-xl ${
                  msg.role === 'user' 
                    ? 'bg-[#38BDF8] text-[#0B0F17]' 
                    : 'bg-white/10 text-white'
                }`}>
                  {msg.content}
                </div>
              </div>
            ))}
          </div>

          {/* Input */}
          <div className="px-12 py-6 border-t border-white/10">
            <div className="flex gap-3 max-w-4xl mx-auto">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                placeholder="Ask about a medication..."
                className="flex-1 px-6 py-3 bg-white/10 text-white placeholder:text-gray-500 rounded-lg border border-white/20 focus:outline-none focus:ring-2 focus:ring-[#38BDF8]"
              />
              <button
                onClick={sendMessage}
                className="px-6 py-3 bg-[#38BDF8] text-[#0B0F17] font-semibold rounded-lg hover:bg-[#0EA5E9] transition"
              >
                Send
              </button>
            </div>
          </div>
        </div>
      )}

      {page === 'login' && (
        <div className="min-h-screen flex items-center justify-center">
          <div className="w-full max-w-md p-8 bg-white/5 rounded-2xl">
            <h1 className="text-3xl font-bold mb-6">Login</h1>
            <button 
              onClick={() => setPage('landing')}
              className="w-full px-6 py-3 bg-white text-[#0B0F17] font-semibold rounded-lg hover:bg-gray-200 transition mt-4"
            >
              Back to Home
            </button>
          </div>
        </div>
      )}

      {page === 'signup' && (
        <div className="min-h-screen flex items-center justify-center">
          <div className="w-full max-w-md p-8 bg-white/5 rounded-2xl">
            <h1 className="text-3xl font-bold mb-6">Sign Up</h1>
            <button 
              onClick={() => setPage('landing')}
              className="w-full px-6 py-3 bg-white text-[#0B0F17] font-semibold rounded-lg hover:bg-gray-200 transition mt-4"
            >
              Back to Home
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
