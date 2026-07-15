import React from "react";
import { Bot, FileUp, History, MessageSquareText, TerminalSquare } from "lucide-react";

const navItems = [
  { id: "chat", label: "Chat", icon: MessageSquareText },
  { id: "logs", label: "Analyze", icon: TerminalSquare },
  { id: "upload", label: "Upload", icon: FileUp },
  { id: "history", label: "History", icon: History }
];

export default function Layout({ activePage, onPageChange, children }) {
  return (
    <div className="min-h-screen bg-zinc-100 text-zinc-950">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-zinc-200 bg-white px-4 py-5 md:block">
        <div className="mb-8 flex items-center gap-3">
          <div className="grid size-10 place-items-center rounded bg-emerald-600 text-white">
            <Bot size={22} />
          </div>
          <div>
            <h1 className="text-base font-semibold">DevOps RAG</h1>
            <p className="text-xs text-zinc-500">Junior engineer assistant</p>
          </div>
        </div>
        <nav className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = activePage === item.id;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onPageChange(item.id)}
                className={`flex w-full items-center gap-3 rounded px-3 py-2 text-left text-sm font-medium ${
                  active ? "bg-zinc-900 text-white" : "text-zinc-700 hover:bg-zinc-100"
                }`}
              >
                <Icon size={17} />
                {item.label}
              </button>
            );
          })}
        </nav>
      </aside>
      <header className="sticky top-0 z-10 border-b border-zinc-200 bg-white px-4 py-3 md:hidden">
        <div className="flex items-center gap-2 overflow-x-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onPageChange(item.id)}
                className={`flex shrink-0 items-center gap-2 rounded px-3 py-2 text-sm ${
                  activePage === item.id ? "bg-zinc-900 text-white" : "bg-zinc-100 text-zinc-700"
                }`}
              >
                <Icon size={16} />
                {item.label}
              </button>
            );
          })}
        </div>
      </header>
      <main className="md:pl-64">
        <div className="mx-auto max-w-6xl px-4 py-6 md:px-8">{children}</div>
      </main>
    </div>
  );
}
