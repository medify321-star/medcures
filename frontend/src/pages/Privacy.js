import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { ScrollArea } from '../components/ui/scroll-area';
import { ArrowLeft } from 'lucide-react';

const Privacy = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[#0B0F17] relative">
      <div 
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: 'url(https://images.unsplash.com/photo-1607893326676-5c46ba36251f?crop=entropy&cs=srgb&fm=jpg&q=85)',
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }}
      />

      <div className="relative z-10">
        <header className="px-6 md:px-12 py-6 border-b border-white/10">
          <Button
            variant="ghost"
            onClick={() => navigate('/')}
            className="text-slate-300 hover:text-white hover:bg-white/5"
            data-testid="back-button"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Home
          </Button>
        </header>

        <ScrollArea className="h-[calc(100vh-100px)]">
          <div className="max-w-4xl mx-auto px-6 md:px-12 py-12 space-y-8 text-white">
            <h1 className="text-4xl font-normal" data-testid="privacy-heading">Privacy Policy</h1>
            <p className="text-slate-400">Last updated: January 2026</p>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">1. Information We Collect</h2>
              <p className="text-slate-300 leading-relaxed">
                We collect information that you provide directly to us, including:
              </p>
              <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
                <li>Account information (email, name, password)</li>
                <li>Chat messages and queries</li>
                <li>Feedback and ratings</li>
                <li>Usage data and preferences</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">2. How We Use Your Information</h2>
              <p className="text-slate-300 leading-relaxed">
                We use the information we collect to:
              </p>
              <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
                <li>Provide and improve our services</li>
                <li>Respond to your queries with relevant medical information</li>
                <li>Send important updates and notifications</li>
                <li>Analyze usage patterns to enhance user experience</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">3. Data Storage and Security</h2>
              <p className="text-slate-300 leading-relaxed">
                We implement appropriate security measures to protect your personal information:
              </p>
              <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
                <li>Encrypted storage of chat history (last 5 chats per user)</li>
                <li>Secure password hashing</li>
                <li>Regular security audits</li>
                <li>Limited data retention policies</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">4. Data Sharing</h2>
              <p className="text-slate-300 leading-relaxed">
                We do NOT sell, trade, or rent your personal information to third parties. Feedback data is accessible only to authorized administrators for quality improvement purposes.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">5. Your Rights (GDPR Compliance)</h2>
              <p className="text-slate-300 leading-relaxed">
                You have the right to:
              </p>
              <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
                <li>Access your personal data</li>
                <li>Request correction of inaccurate data</li>
                <li>Request deletion of your account and data</li>
                <li>Object to data processing</li>
                <li>Data portability</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">6. Medical Information Disclaimer</h2>
              <p className="text-slate-300 leading-relaxed">
                We do NOT store personal health information. All information provided is for educational purposes only. We are not responsible for any medical decisions made based on information from our platform.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">7. Contact Us</h2>
              <p className="text-slate-300 leading-relaxed">
                For privacy-related questions or to exercise your rights, contact us at: medcures15@gmail.com
              </p>
            </section>
          </div>
        </ScrollArea>
      </div>
    </div>
  );
};

export default Privacy;