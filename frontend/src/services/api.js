import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_URL,
});

export const uploadPDF = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await API.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
};

export const askQuestion = async (question) => {
  const response = await API.post("/ask", {
    question,
  });

  return response.data;
};