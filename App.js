import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [input, setInput] = useState("");
  const [generatedPrompt, setGeneratedPrompt] = useState("");

  const generatePrompt = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/generate", {
        input,  // 這裡要與後端的 `input` 字段對應
      });

      setGeneratedPrompt(response.data.generated_prompt);
    } catch (error) {
      console.error("❌ 生成失敗", error);
      setGeneratedPrompt("⚠️ 無法生成 Prompt，請檢查後端是否運行");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100">
      <div className="bg-white shadow-lg p-6 rounded-lg w-96">
        <h1 className="text-2xl font-bold text-center mb-4">🚀 AI Prompt Generator</h1>

        <input
          type="text"
          placeholder="輸入主題或描述"
          className="w-full p-2 border rounded"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />

        <button
          onClick={generatePrompt}
          className="w-full bg-blue-500 text-white p-2 mt-3 rounded hover:bg-blue-600"
        >
          生成 Prompt
        </button>

        {generatedPrompt && (
          <div className="mt-4 p-3 bg-gray-100 rounded">
            <h2 className="font-semibold">🎯 生成的 Prompt:</h2>
            <p className="text-gray-700">{generatedPrompt}</p>
          </div>
        )}
      </div>
    </div>
  );
}
