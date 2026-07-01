import "./AnswerCard.css";
import SourceCard from "./SourceCard";
import ReactMarkdown from "react-markdown";
import { CheckCircle, ShieldCheck, Files } from "lucide-react";

function AnswerCard({ result }) {
  return (
    <div className="answer-card">
      <h2>Answer</h2>

      <div className="answer-text">
        <ReactMarkdown>{result.answer}</ReactMarkdown>
      </div>

      <div className="metrics">
        {/* Confidence */}
        <div className="metric">
          <CheckCircle size={18} />

          <div>
            <span>Confidence</span>
            <h4>{result.confidence ?? "--"}%</h4>
          </div>
        </div>

        {/* Hallucination */}
        <div className="metric">
          <ShieldCheck size={18} />

          <div>
            <span>Hallucination</span>
            <h4 className={result.hallucination ? "warning-text" : "success-text"}>
  {result.hallucination ? "Detected" : "Not Detected"}
</h4>
          </div>
        </div>

        {/* Sources Used */}
        <div className="metric">
          <Files size={18} />

          <div>
            <span>Sources Used</span>
            <h4>{result.chunks_used} Chunks</h4>
          </div>
        </div>
      </div>

      <h3 className="source-title">Source Citations</h3>

      <div className="source-list">
        {result.sources?.length ? (
          result.sources.map((source, index) => (
            <SourceCard key={index} source={source} />
          ))
        ) : (
          <p>No citations available.</p>
        )}
      </div>
    </div>
  );
}

export default AnswerCard;