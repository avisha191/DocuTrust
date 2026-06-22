import { useState } from "react";
import API from "../services/api";

function ChatSection() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {

    const res = await API.post("/ask", {
      question
    });

    setAnswer(res.data.answer);
  };

  return (
    <div>

      <textarea
        placeholder="Ask your PDF anything..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>
        Ask
      </button>

      <div>
        <h3>Answer</h3>
        <p>{answer}</p>
      </div>

    </div>
  );
}

export default ChatSection;