import { useState } from "react";

import "./Home.css";

import Navbar from "../components/Navbar";
import UploadSection from "../components/UploadSection";
import AgentPipeline from "../components/AgentPipeline";
import ChatSection from "../components/ChatSection";

function Home() {

  const [pipelineStatus, setPipelineStatus] = useState({});

  return (
    <>
      <Navbar />

      <div className="home">

        <div className="top-section">

          <div className="left-panel">

            <UploadSection
              setPipelineStatus={setPipelineStatus}
            />

          </div>

          <div className="right-panel">

            <AgentPipeline
              status={pipelineStatus}
            />

          </div>

        </div>

        <div className="bottom-section">

          <ChatSection />

        </div>

      </div>
    </>
  );
}

export default Home;