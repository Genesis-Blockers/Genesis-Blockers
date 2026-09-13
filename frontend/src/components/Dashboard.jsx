import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Shield, LayoutDashboard, Activity, Settings, LogOut } from 'lucide-react';

const DUMMY_LOGS = [
  "> [SYS] Rerouting node 0x4a...",
  "> [WARN] High-volume mixer deposit detected",
  "> [INFO] Block #184293 analyzed",
  "> [NET] Mempool sync: OK",
  "> [TRACE] Calculating heuristic confidence...",
  "> [SYS] Monitoring mempool for flagged addresses...",
  "> [OK] Connected to mainnet node array.",
  "> [WARN] Suspicious contract interaction intercepted.",
  "> [INFO] VASP heuristic engine updated.",
  "> [SYS] 14 nodes mapped in background queue.",
  "> [TRACE] Identifying nested clustering patterns.",
  "> [NET] Handshake verified with off-shore exchange.",
  "> [WARN] Cross-chain bridge hop detected.",
  "> [INFO] Extracting metadata from tx payload...",
  "> [SYS] Anomaly detection threshold adjusted.",
  "> [OK] Local ledger synced.",
];

const RECENT_CASES = [
  {
    id: "INV-2026-0001",
    chain: "ETH",
    targetFull: "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    status: "CLOSED",
    statusStyle: "bg-slate-900 border border-slate-800 text-slate-500"
  },
  {
    id: "INV-2026-0002",
    chain: "BTC",
    targetFull: "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
    status: "ACTIVE",
    statusStyle: "border border-emerald-500/30 text-emerald-400 bg-emerald-500/10 shadow-[0_0_8px_rgba(16,185,129,0.2)]"
  },
  {
    id: "INV-2026-0003",
    chain: "TRX",
    targetFull: "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb",
    status: "CLOSED",
    statusStyle: "bg-slate-900 border border-slate-800 text-slate-500"
  }
];

const truncateAddress = (addr) => `${addr.slice(0, 6)}...${addr.slice(-4)}`;

const Dashboard = () => {
  const navigate = useNavigate();
  const [logs, setLogs] = useState([
    "> [SYS] Monitoring mempool for flagged addresses...",
    "> [OK] Connected to mainnet node array.",
    "> [INFO] VASP heuristic engine updated.",
  ]);

  useEffect(() => {
    let timeoutId;
    
    const addLog = () => {
      const randomLog = DUMMY_LOGS[Math.floor(Math.random() * DUMMY_LOGS.length)];
      
      setLogs(prev => {
        const newLogs = [...prev, randomLog];
        // Keep max 7 items so it acts as a scrolling queue
        if (newLogs.length > 7) {
          return newLogs.slice(newLogs.length - 7);
        }
        return newLogs;
      });
      
      // Randomize interval between 1200ms and 2000ms
      const nextTick = Math.floor(Math.random() * (2000 - 1200 + 1)) + 1200;
      timeoutId = setTimeout(addLog, nextTick);
    };

    // Start loop
    timeoutId = setTimeout(addLog, 1500);

    return () => clearTimeout(timeoutId);
  }, []);

  return (
    <div className="h-screen w-full flex bg-slate-900 text-slate-200">
      
      {/* Arc-Style Sidebar */}
      <div className="w-16 flex-none bg-slate-950 border-r border-slate-800 flex flex-col items-center py-6 space-y-8 z-10">
        <Shield className="w-6 h-6 text-blue-500" />
        
        <div className="flex flex-col space-y-6 flex-1 items-center mt-4">
          <button className="p-2 bg-slate-800/50 rounded-lg text-slate-100" title="Dashboard">
            <LayoutDashboard className="w-5 h-5" />
          </button>
          <button className="p-2 text-slate-500 hover:text-slate-300 transition-colors" title="Activity">
            <Activity className="w-5 h-5" />
          </button>
        </div>

        <div className="flex flex-col space-y-6 items-center">
          <button className="p-2 text-slate-500 hover:text-slate-300 transition-colors" title="Settings">
            <Settings className="w-5 h-5" />
          </button>
          <button 
            className="p-2 text-slate-500 hover:text-slate-300 transition-colors"
            onClick={() => navigate('/login')}
            title="Log Out"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-8 overflow-y-auto bg-[#0b0f19]">
        
        {/* Header */}
        <div>
          <p className="text-[10px] uppercase tracking-widest text-blue-500 font-mono mb-2">
            OPERATOR CONSOLE
          </p>
          <h1 className="text-3xl text-slate-100 font-semibold tracking-tight">
            Welcome back, Agent OP-7742-X
          </h1>
        </div>

        {/* Global Targeting Command (Top Banner) */}
        <div className="bg-slate-950 border border-slate-800 p-6 rounded-lg flex flex-col xl:flex-row xl:justify-between xl:items-center mt-10 shadow-sm">
          <div>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(16,185,129,0.8)]"></div>
              <h2 className="text-lg font-mono text-slate-200">Targeting Console</h2>
            </div>
            <p className="text-sm font-mono text-slate-400 mt-1">Awaiting target coordinates.</p>
          </div>
          <div className="mt-6 xl:mt-0 flex flex-col sm:flex-row items-stretch sm:items-center space-y-4 sm:space-y-0 sm:space-x-4">
            
            <div className="flex items-center gap-3 w-full sm:w-[28rem]">
              <select className="bg-[#020617] border border-blue-900/50 text-blue-400 font-mono text-sm px-3 py-2 rounded focus:outline-none focus:border-blue-500 cursor-pointer">
                <option value="ETH">ETH</option>
                <option value="BTC">BTC</option>
                <option value="TRX">TRX</option>
                <option value="SOL">SOL</option>
                <option value="POLYGON">POLYGON</option>
                <option value="BNB">BNB</option>
              </select>
              <input 
                placeholder="Enter target address (0x..., bc1..., 3...)..." 
                className="bg-[#020617] border border-blue-900/50 text-blue-400 font-mono text-sm flex-1 px-4 py-2 rounded focus:outline-none focus:border-blue-500 transition-all" 
              />
            </div>

            <button 
              className="bg-blue-600 hover:bg-blue-500 text-white py-2.5 px-6 rounded hover:shadow-[0_0_15px_rgba(37,99,235,0.5)] transition-all duration-300 font-mono text-sm whitespace-nowrap flex-shrink-0"
              onClick={() => navigate('/investigate')}
            >
              &gt;_ INITIATE TRACE
            </button>
          </div>
        </div>

        {/* HUD Targeting Brackets (Metrics Row) */}
        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="relative bg-[#020617] border border-slate-800 p-6 rounded-lg border-t-2 border-t-blue-500/50 hover:-translate-y-1 hover:border-blue-500/30 transition-all duration-300 cursor-default shadow-lg shadow-black/50">
            {/* Corner Accents */}
            <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-blue-400 rounded-tl"></div>
            <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-blue-400 rounded-tr"></div>
            <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-blue-400 rounded-bl"></div>
            <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-blue-400 rounded-br"></div>
            
            <p className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-2">Active Traces</p>
            <p className="text-4xl font-mono mt-2 text-slate-200">12</p>
          </div>

          <div className="relative bg-[#020617] border border-slate-800 p-6 rounded-lg border-t-2 border-t-blue-500/50 hover:-translate-y-1 hover:border-blue-500/30 transition-all duration-300 cursor-default shadow-lg shadow-black/50">
            {/* Corner Accents */}
            <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-blue-400 rounded-tl"></div>
            <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-blue-400 rounded-tr"></div>
            <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-blue-400 rounded-bl"></div>
            <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-blue-400 rounded-br"></div>
            
            <p className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-2">VASP Matches</p>
            <p className="text-4xl font-mono mt-2 text-slate-200">142</p>
          </div>

          <div className="relative bg-[#020617] border border-slate-800 p-6 rounded-lg border-t-2 border-t-red-500/50 hover:-translate-y-1 hover:border-red-500/30 transition-all duration-300 cursor-default shadow-lg shadow-black/50">
            {/* Corner Accents - Red for elevated threat */}
            <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-red-400 rounded-tl"></div>
            <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-red-400 rounded-tr"></div>
            <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-red-400 rounded-bl"></div>
            <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-red-400 rounded-br"></div>
            
            <p className="text-xs font-mono text-slate-500 uppercase tracking-wider mb-2">Threat Level</p>
            <p className="text-4xl font-mono mt-2 text-red-500 drop-shadow-[0_0_8px_rgba(239,68,68,0.8)]">ELEVATED</p>
          </div>
        </div>

        {/* Split Bottom Layout */}
        <div className="mt-10 grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left side (Col-span-2) - Case Ledger */}
          <div className="lg:col-span-2 flex flex-col">
            <h3 className="text-sm font-mono text-slate-300 uppercase tracking-wider mb-4 border-b border-slate-800/50 pb-2">
              Recent Activity
            </h3>
            <div className="space-y-3 flex-1 min-h-[280px]">
              
              {RECENT_CASES.map(c => (
                <div 
                  key={c.id} 
                  className="group cursor-pointer hover:bg-blue-900/10 hover:border-l-blue-500 border-l-2 border-l-transparent bg-slate-950 border border-slate-800 rounded-r p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between transition-colors duration-200"
                  onClick={() => navigate('/investigate')}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-4 mb-3 sm:mb-0">
                    <div className="flex items-center mb-1 sm:mb-0">
                      <span className="text-[10px] bg-blue-500/10 text-blue-400 border border-blue-500/30 px-1.5 py-0.5 rounded font-mono mr-2">
                        {c.chain}
                      </span>
                      <span className="font-mono text-blue-400 text-sm">{c.id}</span>
                    </div>
                    <span className="text-slate-400 text-sm font-mono flex items-center">
                      Target:
                      <span className="ml-2">
                        <span className="inline group-hover:hidden text-slate-400">
                          {truncateAddress(c.targetFull)}
                        </span>
                        <span className="hidden group-hover:inline text-blue-400 drop-shadow-[0_0_5px_rgba(96,165,250,0.8)] transition-all">
                          {c.targetFull}
                        </span>
                        <span 
                          className="hidden group-hover:inline ml-2 text-[10px] text-emerald-500 hover:text-emerald-400 active:text-emerald-300 transition-colors font-bold"
                          onClick={(e) => {
                            e.stopPropagation();
                            navigator.clipboard.writeText(c.targetFull);
                          }}
                        >
                          [COPY]
                        </span>
                      </span>
                    </span>
                  </div>
                  <div className={`self-start sm:self-auto px-2 py-1 rounded text-xs font-mono ${c.statusStyle}`}>
                    {c.status}
                  </div>
                </div>
              ))}

            </div>
          </div>

          {/* Right side (Col-span-1) - Live Terminal */}
          <div className="lg:col-span-1 flex flex-col">
            <h3 className="text-sm font-mono text-slate-300 uppercase tracking-wider mb-4 border-b border-slate-800/50 pb-2">
              Live Network Telemetry
            </h3>
            <div className="bg-black border border-slate-800 rounded-lg p-4 min-h-[280px] h-full overflow-hidden relative shadow-inner">
              {/* Subtle Scanline Effect for terminal */}
              <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_4px,3px_100%] z-10 opacity-20"></div>
              
              <div className="text-emerald-500 text-[10px] font-mono leading-relaxed space-y-1 relative z-20">
                {logs.map((log, index) => (
                  <p key={index} className={
                    log.includes('[WARN]') 
                      ? 'text-amber-500 drop-shadow-[0_0_2px_rgba(245,158,11,0.8)]' 
                      : log.includes('[OK]') 
                      ? 'text-emerald-400/80' 
                      : ''
                  }>
                    {log}
                  </p>
                ))}
                <p className="animate-pulse">&gt; _</p>
              </div>
            </div>
          </div>

        </div>
        
      </div>
    </div>
  );
};

export default Dashboard;
