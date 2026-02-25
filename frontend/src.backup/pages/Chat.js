import React, { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { ScrollArea } from '../components/ui/scroll-area';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../components/ui/dialog';
import { toast } from 'sonner';
import { Send, ThumbsUp, ThumbsDown, Copy, Menu, Home, X, MessageSquare } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Chat = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, token, isAuthenticated, guestChatCount, incrementGuestChat } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showDisclaimer, setShowDisclaimer] = useState(true);
  const [showSignupPrompt, setShowSignupPrompt] = useState(false);
  const [showMembershipPrompt, setShowMembershipPrompt] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Check if there's an initial query from landing page
    if (location.state?.initialQuery) {
      setInput(location.state.initialQuery);
    }
  }, [location]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Check guest limit
    if (!isAuthenticated && guestChatCount >= 3) {
      setShowSignupPrompt(true);
      return;
    }

    // Check member limit
    if (isAuthenticated && !user?.is_member && messages.length >= 4) {
      setShowMembershipPrompt(true);
      return;
    }

    const userMessage = { role: 'user', content: input, timestamp: new Date().toISOString() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      const response = await axios.post(
        `${API}/chat/send`,
        { message: input, session_id: sessionId },
        { headers }
      );

      const aiMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date().toISOString(),
        citations: response.data.citations,
        drug_info: response.data.drug_info
      };

      setMessages(prev => [...prev, aiMessage]);
      setSessionId(response.data.session_id);

      // Increment guest chat count
      if (!isAuthenticated) {
        incrementGuestChat();
      }
    } catch (error) {
      console.error('Error sending message:', error);
      toast.error('Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (content) => {
    navigator.clipboard.writeText(content);
    toast.success('Copied to clipboard!');
  };

  const handleFeedback = async (messageIndex, rating) => {
    if (!sessionId) return;

    const message = messages[messageIndex - 1];
    const response = messages[messageIndex];

    try {
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      await axios.post(
        `${API}/feedback/submit`,
        {
          session_id: sessionId,
          message_id: `${sessionId}-${messageIndex}`,
          rating,
          message_content: message.content,
          response_content: response.content
        },
        { headers }
      );
      toast.success('Thank you for your feedback!');
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  return (
    <div className="h-screen bg-[#0B0F17] flex">
      {/* Disclaimer Dialog */}
      <Dialog open={showDisclaimer} onOpenChange={setShowDisclaimer}>
        <DialogContent className="bg-[#151A25] border-white/10 text-white" data-testid="disclaimer-dialog">
          <DialogHeader>
            <DialogTitle className="text-2xl font-normal text-[#38BDF8]">Important Medical Disclaimer</DialogTitle>
            <DialogDescription className="text-slate-300 space-y-4 pt-4">
              <p className="text-base leading-relaxed">
                ⚠️ <strong>Educational Purpose Only:</strong> The information provided by Medcures is for educational and informational purposes only.
              </p>
              <p className="text-base leading-relaxed">
                This platform does NOT provide medical advice, diagnosis, or treatment recommendations. Always consult with a qualified healthcare professional before taking any medication or making health-related decisions.
              </p>
              <p className="text-base leading-relaxed">
                All information is sourced from verified pharmacopoeia databases, but individual medical conditions vary. Professional medical consultation is essential.
              </p>
            </DialogDescription>
          </DialogHeader>
          <Button
            onClick={() => setShowDisclaimer(false)}
            className="w-full bg-[#38BDF8] text-[#0F172A] hover:bg-[#0EA5E9] rounded-full"
            data-testid="accept-disclaimer-button"
          >
            I Understand
          </Button>
        </DialogContent>
      </Dialog>

      {/* Signup Prompt Dialog */}
      <Dialog open={showSignupPrompt} onOpenChange={setShowSignupPrompt}>
        <DialogContent className="bg-[#151A25] border-white/10 text-white" data-testid="signup-prompt-dialog">
          <DialogHeader>
            <DialogTitle className="text-2xl font-normal">Continue Your Journey</DialogTitle>
            <DialogDescription className="text-slate-300 space-y-4 pt-4">
              <p className="text-base">
                You've reached the limit for guest users. Create a free account to continue accessing verified medical information.
              </p>
            </DialogDescription>
          </DialogHeader>
          <div className="flex gap-3">
            <Button
              onClick={() => setShowSignupPrompt(false)}
              variant="outline"
              className="flex-1 border-white/10 text-white hover:bg-white/5"
              data-testid="cancel-signup-button"
            >
              Cancel
            </Button>
            <Button
              onClick={() => navigate('/signup')}
              className="flex-1 bg-[#38BDF8] text-[#0F172A] hover:bg-[#0EA5E9] rounded-full"
              data-testid="goto-signup-button"
            >
              Sign Up
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Membership Prompt Dialog */}
      <Dialog open={showMembershipPrompt} onOpenChange={setShowMembershipPrompt}>
        <DialogContent className="bg-[#151A25] border-white/10 text-white" data-testid="membership-prompt-dialog">
          <DialogHeader>
            <DialogTitle className="text-2xl font-normal">Upgrade to Premium</DialogTitle>
            <DialogDescription className="text-slate-300 space-y-4 pt-4">
              <p className="text-base">
                You are out of limit. Become our member to chat more and access unlimited medical information.
              </p>
            </DialogDescription>
          </DialogHeader>
          <Button
            onClick={() => setShowMembershipPrompt(false)}
            className="w-full bg-[#38BDF8] text-[#0F172A] hover:bg-[#0EA5E9] rounded-full"
            data-testid="close-membership-button"
          >
            Got It
          </Button>
        </DialogContent>
      </Dialog>

      {/* Sidebar */}
      {sidebarOpen && (
        <div className="w-64 bg-[#0B0F17] border-r border-white/10 flex flex-col" data-testid="chat-sidebar">
          <div className="p-4 border-b border-white/10 flex justify-between items-center">
            <h2 className="text-white font-normal">Chat History</h2>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(false)}
              className="text-slate-400 hover:text-white"
              data-testid="close-sidebar-button"
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          <ScrollArea className="flex-1 p-4">
            <div className="space-y-2">
              {sessionId && (
                <div className="p-3 rounded-lg bg-white/5 hover:bg-white/10 cursor-pointer transition-colors" data-testid="current-session">
                  <MessageSquare className="h-4 w-4 inline mr-2 text-[#38BDF8]" />
                  <span className="text-sm text-slate-300">Current Session</span>
                </div>
              )}
            </div>
          </ScrollArea>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-[#151A25] border-b border-white/10 px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-slate-300 hover:text-white hover:bg-white/5"
              data-testid="toggle-sidebar-button"
            >
              <Menu className="h-5 w-5" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate('/')}
              className="text-slate-300 hover:text-white hover:bg-white/5"
              data-testid="home-button"
            >
              <Home className="h-5 w-5" />
            </Button>
          </div>
          {isAuthenticated && (
            <div className="text-sm text-slate-400" data-testid="user-info">
              {user?.name}
            </div>
          )}
        </header>

        {/* Messages */}
        <ScrollArea className="flex-1 px-6 py-8">
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.length === 0 && (
              <div className="text-center text-slate-400 py-12" data-testid="empty-state">
                <p className="text-lg">Start a conversation about any medication</p>
                <p className="text-sm mt-2">Ask about Aspirin, Paracetamol, Amoxicillin, or Ibuprofen</p>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                data-testid={`message-${message.role}-${index}`}
              >
                <div className={`max-w-[80%] ${message.role === 'user' ? 'bg-[#38BDF8] text-[#0F172A]' : 'glass-effect text-white'} rounded-2xl p-4 space-y-3`}>
                  <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
                  
                  {message.citations && (
                    <div className="text-xs opacity-70 border-t border-white/10 pt-2" data-testid={`citations-${index}`}>
                      <strong>Sources:</strong> {message.citations.join(', ')}
                    </div>
                  )}

                  {message.role === 'assistant' && (
                    <div className="flex gap-2 pt-2" data-testid={`feedback-buttons-${index}`}>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleFeedback(index, 'positive')}
                        className="h-7 px-2 hover:bg-white/10"
                        data-testid={`thumbs-up-${index}`}
                      >
                        <ThumbsUp className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleFeedback(index, 'negative')}
                        className="h-7 px-2 hover:bg-white/10"
                        data-testid={`thumbs-down-${index}`}
                      >
                        <ThumbsDown className="h-3 w-3" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleCopy(message.content)}
                        className="h-7 px-2 hover:bg-white/10"
                        data-testid={`copy-${index}`}
                      >
                        <Copy className="h-3 w-3" />
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input */}
        <div className="bg-[#151A25] border-t border-white/10 px-6 py-4">
          <div className="max-w-4xl mx-auto flex gap-3">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && handleSendMessage()}
              placeholder="Ask about any medication..."
              disabled={loading}
              className="flex-1 bg-white/5 border-white/10 text-white placeholder:text-slate-500 focus-visible:ring-[#38BDF8]"
              data-testid="chat-input"
            />
            <Button
              onClick={handleSendMessage}
              disabled={loading || !input.trim()}
              className="bg-[#38BDF8] text-[#0F172A] hover:bg-[#0EA5E9] rounded-full px-6"
              data-testid="send-button"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;