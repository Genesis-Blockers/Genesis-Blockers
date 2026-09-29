import React, { useState } from 'react';
import { Search, ZoomIn, ZoomOut, Focus, Check, ShieldAlert, Loader } from 'lucide-react';
import TransactionGraph from './components/TransactionGraph';

function Workspace() {
    const [wallet, setWallet] = useState("0xsuspect");
    const [maxHops, setMaxHops] = useState(5);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const runInvestigation = async () => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch("http://localhost:8000/api/v1/investigate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    wallet: wallet,
                    chain: "ethereum",
                    max_hops: parseInt(maxHops)
                })
            });
            if (!response.ok) {
                throw new Error("Failed to fetch investigation results");
            }
            const data = await response.json();
            setResult(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="h-screen w-full flex flex-col font-sans bg-slate-950 text-slate-200 overflow-hidden">

            {/* 1. Top Search Workspace (Header) */}
            <header className="flex-none flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/50 backdrop-blur-sm z-10">
                <div className="flex items-center space-x-6 w-full max-w-5xl">
                    <div className="flex items-center space-x-2">
                        <ShieldAlert className="w-6 h-6 text-blue-500" />
                        <h1 className="text-lg font-semibold tracking-tight text-slate-100">Genesis Blockers</h1>
                    </div>

                    <div className="flex-1 flex items-center space-x-3 bg-slate-900/50 p-1.5 rounded-md border border-slate-800/50">
                        <div className="flex-1 relative">
                            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                            <input
                                type="text"
                                placeholder="0x..."
                                className="w-full bg-slate-900 border border-slate-700 rounded-sm py-1.5 pl-9 pr-3 text-sm font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors"
                                value={wallet}
                                onChange={(e) => setWallet(e.target.value)}
                            />
                        </div>

                        <select
                            disabled
                            className="bg-slate-900 border border-slate-700 rounded-sm py-1.5 px-3 text-sm text-slate-400 opacity-70 cursor-not-allowed appearance-none"
                        >
                            <option>Ethereum</option>
                        </select>

                        <div className="flex items-center space-x-2 px-2 border-l border-slate-800">
                            <label className="text-xs text-slate-400 font-medium whitespace-nowrap">Max Hops</label>
                            <input
                                type="number"
                                min="1" max="20"
                                className="w-16 bg-slate-900 border border-slate-700 rounded-sm py-1 text-center text-sm text-slate-200 focus:outline-none focus:border-blue-500"
                                value={maxHops}
                                onChange={(e) => setMaxHops(e.target.value)}
                            />
                        </div>

                        <button 
                            onClick={runInvestigation}
                            disabled={loading}
                            className="bg-slate-800 border border-slate-700 text-slate-200 hover:bg-slate-700 px-4 py-1.5 rounded-sm text-sm font-medium transition-colors whitespace-nowrap disabled:opacity-50 flex items-center gap-2">
                            {loading && <Loader className="w-4 h-4 animate-spin" />}
                            Run Investigation
                        </button>
                    </div>
                </div>
            </header>

            {/* Main Workspace */}
            <main className="flex-1 flex overflow-hidden">

                {/* 2. Main Workspace - Left Pane (Graph Canvas) */}
                <section className="relative w-[70%] h-full bg-slate-900 border-r border-slate-800 flex flex-col">
                    <TransactionGraph result={result} />

                    {/* Floating Control Overlay */}
                    <div className="absolute bottom-6 left-6 z-20 flex flex-col bg-slate-950 border border-slate-800 rounded-md shadow-xl overflow-hidden">
                        <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors border-b border-slate-800" title="Zoom In">
                            <ZoomIn className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors border-b border-slate-800" title="Zoom Out">
                            <ZoomOut className="w-4 h-4" />
                        </button>
                        <button className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors" title="Recenter">
                            <Focus className="w-4 h-4" />
                        </button>
                    </div>
                </section>

                {/* 3. Main Workspace - Right Pane (Attribution Sidebar) */}
                <aside className="w-[30%] h-full bg-slate-950 p-5 overflow-y-auto custom-scrollbar flex flex-col space-y-6">

                    {/* Investigation Summary Card */}
                    <div className="flex flex-col space-y-1 pb-4 border-b border-slate-800/50">
                        <div className="flex items-center justify-between">
                            <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Investigation</h2>
                            <span className="text-xs font-mono text-slate-500">{result ? result.investigation_id : "INV-XXXX-XXXX"}</span>
                        </div>
                        <p className="text-sm text-slate-500 mt-2">
                            {result && <span className="text-slate-300 font-medium">{result.message}</span>}
                            {error && <span className="text-red-400 font-medium">{error}</span>}
                            {!result && !error && <span>Enter a wallet to investigate</span>}
                        </p>
                    </div>

                    {/* Dynamic VASPs List */}
                    {result && result.attributions && result.attributions.map((attr, idx) => (
                        <div key={idx} className="bg-slate-900/50 border border-slate-800 rounded-md p-4 flex flex-col space-y-4">
                            <div className="flex items-start justify-between">
                                <div>
                                    <h3 className="text-sm font-medium text-slate-400">VASP Match #{idx + 1} ({attr.vasp_category})</h3>
                                    <p className="text-2xl font-semibold text-slate-100 mt-1 tracking-tight">{attr.vasp_name}</p>
                                    <p className="text-xs font-mono text-slate-500 mt-1">{attr.matched_address}</p>
                                </div>
                                <div className={`text-xs font-bold px-2 py-1 rounded shadow-sm ${attr.risk_score > 70 ? 'bg-red-500/10 border-red-500/20 text-red-400' : 'bg-orange-500/10 border-orange-500/20 text-orange-400'}`}>
                                    RISK: {attr.risk_score}
                                </div>
                            </div>

                            <div className="flex items-center space-x-4 pt-2">
                                <div className="flex flex-col">
                                    <span className="text-xs text-slate-500">Confidence</span>
                                    <span className="text-lg font-mono text-emerald-400">{attr.confidence_score}%</span>
                                </div>
                                <div className="w-px h-8 bg-slate-800"></div>
                                <div className="flex flex-col">
                                    <span className="text-xs text-slate-500">Graph Distance</span>
                                    <span className="text-lg font-mono text-slate-200">{attr.path.hops} Hops</span>
                                </div>
                                <div className="w-px h-8 bg-slate-800"></div>
                                <div className="flex flex-col">
                                    <span className="text-xs text-slate-500">Value Transferred</span>
                                    <span className="text-lg font-mono text-slate-200">{attr.path.total_value.toFixed(2)} ETH</span>
                                </div>
                            </div>

                            <div className="flex flex-col space-y-2 pt-3 border-t border-slate-800/50">
                                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Path</h4>
                                <div className="text-xs text-slate-300 font-mono bg-slate-950 p-2 rounded max-h-32 overflow-y-auto">
                                    {attr.path.path.join(" ➔ ")}
                                </div>
                            </div>
                        </div>
                    ))}

                </aside>
            </main>
        </div>
    );
}

export default Workspace;
