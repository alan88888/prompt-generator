import os
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
# Flask 伺服器
app = Flask(__name__)
CORS(app)

# 本地 LLM API 位置
LLM_API_URL = "http://127.0.0.1:1234/v1/chat/completions"

# 預設模型名稱（請確認你的模型名稱是否正確）
MODEL_NAME = "hermes-3-llama-3.2-3b"

@app.route("/generate", methods=["POST"])
def generate_prompt():
    """接收用戶請求，並返回 AI 生成的 Prompt"""
    data = request.json
    user_input = data.get("input", "").strip()

    if not user_input:
        return jsonify({"error": "請提供有效的輸入"}), 400

    print(f"👤 使用者輸入：{user_input}")

    # **System 訊息 - 讓 LLM 成為專業 Prompt 生成器**
    system_message = {
        "role": "system",
        "content": (
            "你是一個專業的創意發想生成器，負責為使用者的輸入做出極具創意與各有差異的點子，但還是要盡可能符合現實。\n"
            "<think>你需要考慮使用者的完整輸入，生成對於該完整輸入包括多種不同面向與發想的回答，可以是專業的答覆、抽象的描述，抑或是有趣的故事。</think>\n"
            "各回答之間的差異性越遠越好，最好是完全不同性質與意涵的答覆。\n"
            "<think>請至多生成4到5個例子，並且每一點都簡短說明，每點濃縮於80字內，用繁體中文字回答。</think>"
        )
    }

    # 建立 LLM 請求格式
    llm_payload = {
        "model": MODEL_NAME,
        "messages": [
            system_message,
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "stream": False
    }

    try:
        # 呼叫本地 LLM
        response = requests.post(LLM_API_URL, json=llm_payload)

        # 檢查回應
        if response.status_code == 200:
            llm_response = response.json()
            ai_reply = llm_response.get("choices", [{}])[0].get("message", {}).get("content", "")
        else:
            print(f"❌ LLM API 錯誤: {response.text}")
            return jsonify({"error": "LLM 無法生成 Prompt"}), 500

    except Exception as e:
        print(f"❌ LLM API 連線失敗: {e}")
        return jsonify({"error": "無法連接到 LLM"}), 500

    print(f"🤖 AI 生成的 Prompt：{ai_reply}")
    return jsonify({"generated_prompt": ai_reply})

# 啟動 Flask 伺服器
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
