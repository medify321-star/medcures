import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Search, Shield, BookOpen, Sparkles } from 'lucide-react';

const Landing = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate('/chat', { state: { initialQuery: searchQuery } });
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F17] relative overflow-hidden">
      {/* Background texture */}
      <div 
        className="absolute inset-0 opacity-30"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1607893326676-5c46ba36251f?crop=entropy&cs=srgb&fm=jpg&q=85)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      />
      
      {/* Gradient overlay */}
      <div className="absolute inset-0" style={{
        background: 'radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.15) 0%, rgba(11, 15, 23, 0) 70%)'
      }} />

      {/* Content */}
      <div className="relative z-10">
        {/* Header */}
        <header className="flex justify-between items-center px-6 md:px-12 py-6">
          <div></div>
          <div className="flex gap-3">
            <Button 
              variant="ghost" 
              onClick={() => navigate('/login')}
              className="text-slate-200 hover:text-white hover:bg-white/5"
              data-testid="login-button"
            >
              Login
            </Button>
            <Button 
              onClick={() => navigate('/signup')}
              className="bg-[#38BDF8] text-[#0F172A] hover:bg-[#0EA5E9] rounded-full px-6 shadow-[0_0_20px_rgba(56,189,248,0.3)]"
              data-testid="signup-button"
            >
              Sign Up
            </Button>
          </div>
        </header>

        {/* Hero Section */}
        <main className="flex flex-col items-center justify-center min-h-[calc(100vh-120px)] px-6 md:px-12">
          <div className="max-w-4xl w-full text-center space-y-8 animate-in fade-in duration-700">
            <h1 className="text-4xl md:text-6xl font-normal tracking-tight text-white leading-tight" data-testid="hero-heading">
              Your Trusted Medical Information
              <span className="block mt-2 text-[#38BDF8]">Companion</span>
            </h1>
            
            <p className="text-lg md:text-xl text-slate-300 leading-relaxed max-w-2xl mx-auto" data-testid="hero-description">
              Get verified pharmaceutical information from trusted sources. Educational guidance for informed healthcare decisions.
            </p>

            {/* Search Bar - Key Feature */}
            <form onSubmit={handleSearch} className="w-full max-w-3xl mx-auto mt-12" data-testid="search-form">
              <div className="relative">
                <Search className="absolute left-6 top-1/2 -translate-y-1/2 h-5 w-5 text-slate-500" />
                <Input
                  type="text"
                  placeholder="Ask about any medication... (e.g., Aspirin, Paracetamol)"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full h-14 pl-14 pr-6 text-lg bg-[#F1F5F9] text-slate-900 placeholder:text-slate-500 border-none rounded-[34px] shadow-lg focus-visible:ring-2 focus-visible:ring-[#38BDF8]/50 focus-visible:ring-offset-0"
                  data-testid="search-input"
                />
              </div>
            </form>

            {/* Quick Info Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16 pt-8">
              <div className="glass-effect rounded-2xl p-6 text-left transition-all duration-300 hover:bg-white/10" data-testid="feature-card-verified">
                <Shield className="h-10 w-10 text-[#38BDF8] mb-4" />
                <h3 className="text-xl font-normal text-white mb-2">Verified Sources</h3>
                <p className="text-sm text-slate-400">Information from British Pharmacopoeia, USP, and FDA databases</p>
              </div>

              <div className="glass-effect rounded-2xl p-6 text-left transition-all duration-300 hover:bg-white/10" data-testid="feature-card-educational">
                <BookOpen className="h-10 w-10 text-[#2DD4BF] mb-4" />
                <h3 className="text-xl font-normal text-white mb-2">Educational Purpose</h3>
                <p className="text-sm text-slate-400">Professional medical information for learning and reference</p>
              </div>

              <div className="glass-effect rounded-2xl p-6 text-left transition-all duration-300 hover:bg-white/10" data-testid="feature-card-ai">
                <Sparkles className="h-10 w-10 text-[#6366F1] mb-4" />
                <h3 className="text-xl font-normal text-white mb-2">AI-Powered</h3>
                <p className="text-sm text-slate-400">Smart responses with proper citations and disclaimers</p>
              </div>
            </div>
          </div>
        </main>

        {/* Footer */}
        <footer className="text-center py-6 text-sm text-slate-500">
          <p>
            <button onClick={() => navigate('/privacy')} className="hover:text-[#38BDF8] transition-colors" data-testid="privacy-link">Privacy Policy</button>
            {' · '}
            <button onClick={() => navigate('/terms')} className="hover:text-[#38BDF8] transition-colors" data-testid="terms-link">Terms & Conditions</button>
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Landing;