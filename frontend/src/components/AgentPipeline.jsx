import "./AgentPipeline.css";
import {
  Upload,
  Scissors,
  Brain,
  Database,
  Search,
  RefreshCw,
  ShieldCheck,
} from "lucide-react";

const icons = {
  upload: <Upload size={18} />,
  chunking: <Scissors size={18} />,
  embedding: <Brain size={18} />,
  retrieval: <Database size={18} />,
  rerank: <Search size={18} />,
  rewrite: <RefreshCw size={18} />,
  hallucination: <ShieldCheck size={18} />,
};

const labels = {
  upload: "Upload",
  chunking: "Chunking",
  embedding: "Embeddings",
  retrieval: "FAISS Retrieval",
  rerank: "CrossEncoder",
  rewrite: "Query Rewrite",
  hallucination: "Hallucination Check",
};

function AgentPipeline({ status = {} }) {
  const steps = Object.keys(labels);

  return (
    <div className="pipeline-card">

      <h2>AI Agent Pipeline</h2>

      <p className="pipeline-subtitle">
        Corrective RAG Workflow
      </p>

      <div className="pipeline-list">

        {steps.map((step) => (

          <div className="pipeline-item" key={step}>

            <div className="pipeline-icon">

              {icons[step]}

            </div>

            <div className="pipeline-text">

              <h4>{labels[step]}</h4>

              <p>{status[step] || "Waiting..."}</p>

            </div>

            <div
              className={`status-circle ${
                status[step] === "Completed"
                  ? "success"
                  : status[step] === "Running"
                  ? "running"
                  : "waiting"
              }`}
            />

          </div>

        ))}

      </div>

    </div>
  );
}

export default AgentPipeline;