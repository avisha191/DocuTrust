import { useState } from "react";
import "./SourceCard.css";

function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="source-card">
      <div className="source-header">
        <h4>Chunk #{source.chunk}</h4>
      </div>

      <div className="source-info">
        <p>
          <strong>Similarity:</strong> {source.similarity}
        </p>

        <p>
          <strong>Rerank Score:</strong> {source.rerank_score}
        </p>
      </div>

      <div className="preview">
        {expanded ? source.full_text : source.preview}
      </div>

      <button
        className="show-more-btn"
        onClick={() => setExpanded(!expanded)}
      >
        {expanded ? "Show Less" : "Show More"}
      </button>
    </div>
  );
}

export default SourceCard;