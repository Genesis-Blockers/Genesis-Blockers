import React from 'react';
import { Search, ZoomIn, ZoomOut, Focus, Check, ShieldAlert } from 'lucide-react';
import TransactionGraph from './components/TransactionGraph';
import AttributionPanel from './components/AttributionPanel';
function Workspace() {
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
                                defaultValue="0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
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
                                min="1" max="20" defaultValue="5"
                                className="w-16 bg-slate-900 border border-slate-700 rounded-sm py-1 text-center text-sm text-slate-200 focus:outline-none focus:border-blue-500"
                            />
                        </div>

                        <button className="bg-slate-800 border border-slate-700 text-slate-200 hover:bg-slate-700 px-4 py-1.5 rounded-sm text-sm font-medium transition-colors whitespace-nowrap">
                            Run Investigation
                        </button>
                    </div>
                </div>
            </header>

            {/* Main Workspace */}
            <main className="flex-1 flex overflow-hidden">

                {/* 2. Main Workspace - Left Pane (Graph Canvas) */}
                <section className="relative w-[70%] h-full bg-slate-900 border-r border-slate-800 flex flex-col">
                    <TransactionGraph />

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
                            <span className="text-xs font-mono text-slate-500">INV-2026-0001</span>
                        </div>
                        <p className="text-sm text-slate-500 mt-2">
                            <span className="text-slate-300 font-medium">4</span> Transactions Analyzed
                        </p>
                    </div>

                    <AttributionPanel />


                </aside>
            </main>
        </div>
    );
}

export default Workspace;
