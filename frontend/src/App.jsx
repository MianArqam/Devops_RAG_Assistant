import React, { useState } from "react";
import Layout from "./components/Layout.jsx";
import ChatPage from "./pages/ChatPage.jsx";
import HistoryPage from "./pages/HistoryPage.jsx";
import LogAnalysisPage from "./pages/LogAnalysisPage.jsx";
import UploadPage from "./pages/UploadPage.jsx";

export default function App() {
  const [activePage, setActivePage] = useState("chat");
  const [history, setHistory] = useState([]);

  function addHistory(item) {
    setHistory((current) => [{ ...item, createdAt: new Date().toISOString() }, ...current].slice(0, 20));
  }

  return (
    <Layout activePage={activePage} onPageChange={setActivePage}>
      {activePage === "chat" && <ChatPage onHistory={addHistory} />}
      {activePage === "logs" && <LogAnalysisPage onHistory={addHistory} />}
      {activePage === "upload" && <UploadPage />}
      {activePage === "history" && <HistoryPage items={history} />}
    </Layout>
  );
}
