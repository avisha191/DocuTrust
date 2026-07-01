import "./Navbar.css";
import { FileText } from "lucide-react";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-left">
        <div className="logo">
          <FileText size={28} />
        </div>

        <div>
          <h1>DocuTrust</h1>
          <p>Enterprise Document Intelligence Platform</p>
        </div>
      </div>

      <div className="navbar-right">
        <span className="status-dot"></span>
        <span>AI Ready</span>
      </div>
    </nav>
  );
}

export default Navbar;