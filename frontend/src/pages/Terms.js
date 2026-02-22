import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { ScrollArea } from '../components/ui/scroll-area';
import { ArrowLeft } from 'lucide-react';

const Terms = () => {
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
            <h1 className="text-4xl font-normal" data-testid="terms-heading">Terms & Conditions</h1>
            <p className="text-slate-400">Last updated: January 2026</p>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">1. Acceptance of Terms</h2>
              <p className="text-slate-300 leading-relaxed">
                By accessing and using Medcures, you accept and agree to be bound by these Terms and Conditions. If you do not agree, please discontinue use immediately.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">2. Educational Purpose Only</h2>
              <p className="text-slate-300 leading-relaxed">
                Medcures provides pharmaceutical information for EDUCATIONAL PURPOSES ONLY. This platform:
              </p>
              <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
                <li>Does NOT provide medical advice, diagnosis, or treatment</li>
                <li>Does NOT replace professional medical consultation</li>
                <li>Should NOT be used for self-diagnosis or self-medication</li>
                <li>Is NOT a substitute for licensed healthcare professionals</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">3. Medical Disclaimer</h2>
              <p className="text-slate-300 leading-relaxed">
                ⚠️ <strong>IMPORTANT:</strong> Always consult with a qualified healthcare professional before taking any medication or making health-related decisions. Individual medical conditions vary, and professional evaluation is essential.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">4. User Responsibilities</h2>
              <p className="text-slate-300 leading-relaxed">
                You agree to:
              </p>
              <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
                <li>Use the platform responsibly and ethically</li>
                <li>Not share false or misleading information</li>
                <li>Maintain confidentiality of your account credentials</li>
                <li>Not attempt to compromise platform security</li>
                <li>Respect intellectual property rights</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">5. Usage Limits</h2>
              <p className="text-slate-300 leading-relaxed">
                Guest users are limited to 3 chat interactions. Registered users have extended access. Premium membership may be required for unlimited usage.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">6. Information Accuracy</h2>
              <p className="text-slate-300 leading-relaxed">
                While we strive to provide accurate information from verified pharmacopoeia sources (British Pharmacopoeia, USP, FDA), we cannot guarantee:
              </p>
              <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
                <li>100% accuracy or completeness of information</li>
                <li>Real-time updates for all medications</li>
                <li>Suitability for specific individual cases</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">7. Limitation of Liability</h2>
              <p className="text-slate-300 leading-relaxed">
                Medcures and its founders are NOT liable for:
              </p>
              <ul className="list-disc list-inside text-slate-300 space-y-2 ml-4">
                <li>Any medical decisions made based on platform information</li>
                <li>Adverse effects from medication use</li>
                <li>Errors or omissions in information provided</li>
                <li>Damages resulting from platform use or inability to use</li>
              </ul>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">8. Intellectual Property</h2>
              <p className="text-slate-300 leading-relaxed">
                All content, design, and technology on Medcures are protected by intellectual property laws. Unauthorized reproduction or distribution is prohibited.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">9. Modifications</h2>
              <p className="text-slate-300 leading-relaxed">
                We reserve the right to modify these terms at any time. Continued use after changes constitutes acceptance of modified terms.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-normal text-[#38BDF8]">10. Contact Information</h2>
              <p className="text-slate-300 leading-relaxed">
                For questions or concerns about these terms, contact us at: medcures15@gmail.com
              </p>
              <p className="text-slate-400 text-sm mt-4">
                Founders: Zainab Bohra & Shriya Soni<br />
                Sponsored by: U.S Ostwal Institute of Pharmacy<br />
                Co-founder: Ishika Chourdiya
              </p>
            </section>
          </div>
        </ScrollArea>
      </div>
    </div>
  );
};

export default Terms;