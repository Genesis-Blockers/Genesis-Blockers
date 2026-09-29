import React from 'react';
import { ShieldAlert, Activity, Terminal, AlertTriangle } from 'lucide-react';

const mlData = {
  "vasp_id": "vasp_binance_01",
  "vasp_name": "Binance",
  "confidence": 0.84,
  "ml_probability": 0.79,
  "baseline_confidence": 0.89,
  "model_version": "rf-v1",
  "attribution_status": "HIGH_CONFIDENCE",
  "risk_score": 32,
  "risk_level": "MEDIUM",
  "reasons": [
    "Candidate is only 1 hop from the input wallet.",
    "Destination address matches a known VASP address.",
    "Address intelligence confidence is high."
  ]
};

const AttributionPanel = () => {
  return (
    <div className="bg-[#020617] border border-blue-900/50 rounded-lg p-4 flex flex-col space-y-6 font-sans shadow-2xl">
      
      {/* Header Area */}
      <div className="flex flex-col space-y-2">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 text-blue-500" />
            <h2 className="text-xl font-bold text-slate-100 tracking-tight">{mlData.vasp_name}</h2>
            <span className="ml-2 px-2 py-0.5 text-[10px] font-bold text-emerald-400 bg-emerald-900/20 border border-emerald-500/30 rounded shadow-[0_0_8px_rgba(16,185,129,0.2)] tracking-wider">
              {mlData.attribution_status}
            </span>
          </div>
          <div className="flex items-center space-x-1 text-slate-500 bg-slate-900/80 px-1.5 py-0.5 rounded border border-slate-800">
            <Terminal className="w-3 h-3" />
            <span className="text-[10px] font-mono">{mlData.model_version}</span>
          </div>
        </div>
        <div className="text-xs text-slate-500 font-mono">
          ID: {mlData.vasp_id}
        </div>
      </div>

      {/* Risk Assessment */}
      <div className="bg-amber-950/20 border border-amber-900/30 rounded-md p-3 flex items-center justify-between shadow-inner">
        <div className="flex items-center space-x-3">
          <AlertTriangle className="w-5 h-5 text-amber-500" />
          <div className="flex flex-col">
            <span className="text-xs font-semibold text-amber-500/70 uppercase tracking-wider">Risk Assessment</span>
            <span className="text-sm font-bold text-amber-400">{mlData.risk_level} RISK</span>
          </div>
        </div>
        <div className="text-right flex flex-col">
          <span className="text-2xl font-mono font-bold text-amber-400">{mlData.risk_score}</span>
          <span className="text-[10px] text-amber-500/50 font-mono uppercase">Score / 100</span>
        </div>
      </div>

      {/* Telemetry/Metrics Grid */}
      <div className="flex flex-col space-y-3">
        <div className="flex items-center space-x-2 border-b border-slate-800 pb-2">
          <Activity className="w-4 h-4 text-slate-400" />
          <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Telemetry Metrics</h3>
        </div>
        
        <div className="grid grid-cols-3 gap-4 pt-1">
          {/* Metric 1 */}
          <div className="flex flex-col space-y-1.5">
            <div className="flex justify-between items-end">
              <span className="text-[10px] text-slate-500 uppercase tracking-wider">Confidence</span>
              <span className="text-xs font-mono text-blue-400">{(mlData.confidence * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)] rounded-full" style={{ width: `${mlData.confidence * 100}%` }}></div>
            </div>
          </div>
          
          {/* Metric 2 */}
          <div className="flex flex-col space-y-1.5">
            <div className="flex justify-between items-end">
              <span className="text-[10px] text-slate-500 uppercase tracking-wider">ML Prob</span>
              <span className="text-xs font-mono text-purple-400">{(mlData.ml_probability * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.5)] rounded-full" style={{ width: `${mlData.ml_probability * 100}%` }}></div>
            </div>
          </div>

          {/* Metric 3 */}
          <div className="flex flex-col space-y-1.5">
            <div className="flex justify-between items-end">
              <span className="text-[10px] text-slate-500 uppercase tracking-wider">Baseline</span>
              <span className="text-xs font-mono text-slate-300">{(mlData.baseline_confidence * 100).toFixed(0)}%</span>
            </div>
            <div className="w-full h-1 bg-slate-800 rounded-full overflow-hidden">
              <div className="h-full bg-slate-400 rounded-full" style={{ width: `${mlData.baseline_confidence * 100}%` }}></div>
            </div>
          </div>
        </div>
      </div>

      {/* Explainability Log */}
      <div className="flex flex-col space-y-2 pt-2">
        <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center">
          <Terminal className="w-3 h-3 mr-1.5" /> Explainability Log
        </h3>
        <div className="bg-slate-900/50 border border-slate-800 rounded p-3 font-mono text-xs flex flex-col space-y-2 shadow-inner">
          {mlData.reasons.map((reason, idx) => (
            <div key={idx} className="flex items-start text-slate-300">
              <span className="text-blue-500 mr-2 shrink-0">{'> [SYS_LOG]:'}</span>
              <span className="leading-relaxed opacity-80">{reason}</span>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
};

export default AttributionPanel;
