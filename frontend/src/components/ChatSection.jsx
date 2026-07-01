import { useState } from "react";
import "./ChatSection.css";
import { askQuestion } from "../services/api";
import AnswerCard from "./AnswerCard";

function ChatSection() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleAsk = async () => {
    if (!question.trim()) return;

    try {
      setLoading(true);

      const response = await askQuestion(question);

      setResult(response);

    } catch (err) {
      console.error(err);

      alert("Failed to get response.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">

      <h2>Ask Your Document</h2>

      <p className="chat-subtitle">
        Query your uploaded documents using Corrective RAG
      </p>

      <div className="chat-input-area">

        <input
          type="text"
          placeholder="Ask anything about your document..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button onClick={handleAsk}>
          {loading ? "Thinking..." : "Ask"}
        </button>

      </div>

      {loading && (
        <div className="loading">
          🤖 AI is analyzing your document...
        </div>
      )}

      {result && (
        <AnswerCard result={result} />
      )}

    </div>
  );
}

export default ChatSection;