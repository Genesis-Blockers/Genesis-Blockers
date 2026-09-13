import React, { useState } from 'react';
import { ShieldAlert, Lock } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    badgeId: '',
    passphrase: '',
    token: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleLogin = (e) => {
    e.preventDefault();
    navigate('/dashboard');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-4 relative overflow-hidden">
      {/* Subtle Dot Pattern Background */}
      <div 
        className="absolute inset-0 z-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage: 'radial-gradient(circle at center, #94a3b8 1px, transparent 1px)',
          backgroundSize: '24px 24px'
        }}
      />

      <div className="w-full max-w-md bg-slate-900/80 backdrop-blur-md border border-slate-700/50 rounded-xl p-8 shadow-2xl relative z-10">
        
        {/* Header section */}
        <div className="flex flex-col items-center mb-8 text-center">
          <div className="bg-blue-900/30 p-3 rounded-full mb-4 border border-blue-800/50 shadow-[0_0_15px_rgba(59,130,246,0.2)]">
            <ShieldAlert className="w-8 h-8 text-blue-500" />
          </div>
          <p className="text-[10px] uppercase tracking-widest text-blue-500 font-mono mb-2">
            RESTRICTED ACCESS
          </p>
          <h1 className="text-xl text-slate-100 font-semibold tracking-wide">
            Genesis Blockers <span className="text-slate-500 mx-1">//</span> Node Authentication
          </h1>
        </div>

        {/* Form */}
        <form onSubmit={handleLogin} className="space-y-5">
          
          <div className="space-y-1.5">
            <label className="block text-[11px] font-mono text-slate-400 ml-1 uppercase tracking-wider">Badge ID / Operator Email</label>
            <input
              type="text"
              name="badgeId"
              value={formData.badgeId}
              onChange={handleChange}
              placeholder="OP-7742-X"
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 text-slate-200 placeholder-slate-600 rounded focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
              required
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-[11px] font-mono text-slate-400 ml-1 uppercase tracking-wider">Passphrase</label>
            <input
              type="password"
              name="passphrase"
              value={formData.passphrase}
              onChange={handleChange}
              placeholder="••••••••••••••••"
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 text-slate-200 placeholder-slate-600 rounded focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
              required
            />
          </div>

          <div className="space-y-1.5">
            <label className="flex items-center text-[11px] font-mono text-slate-400 ml-1 uppercase tracking-wider">
              <Lock className="w-3 h-3 mr-1" />
              2FA Security Token
            </label>
            <input
              type="text"
              name="token"
              value={formData.token}
              onChange={handleChange}
              placeholder="000 000"
              maxLength={6}
              className="w-full px-3 py-2 bg-slate-950 border border-slate-800 text-slate-200 placeholder-slate-600 rounded focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors text-center font-mono tracking-widest text-lg"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-medium py-2.5 rounded transition-colors mt-4 shadow-lg shadow-blue-900/20"
          >
            AUTHORIZE
          </button>
        </form>

        {/* System Warning */}
        <div className="mt-8 pt-4 border-t border-slate-800/50">
          <p className="text-[10px] text-slate-500 text-center font-mono leading-relaxed">
            UNAUTHORIZED ACCESS IS STRICTLY PROHIBITED.<br/>ALL ACTIONS ARE LOGGED.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
