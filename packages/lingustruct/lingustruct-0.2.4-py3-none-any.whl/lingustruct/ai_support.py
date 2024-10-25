import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class AISupport:
    def __init__(self, api_key=None, default_model="llama3-70b-8192"):
        # APIキーの取得
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Groq API key must be provided or set in the GROQ_API_KEY environment variable."
            )

        # Groq APIの初期化
        self.client = Groq(api_key=self.api_key)
        self.default_model = default_model

    def complete_design(
        self,
        section: str,
        content: str,
        model: str = None,
        max_tokens: int = 150,
        temperature: float = 0.7,
        prompt_template: str = None
    ):
        # モデルの選択
        selected_model = model or self.default_model

        # プロンプトの構築
        prompt = prompt_template or (
            f"Complete the following section for system design:\n"
            f"Section: {section}\nContent: {content}\n"
        )

        try:
            # Groq APIを使用したリクエストの送信
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=selected_model,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            # レスポンスから生成されたテキストを取得
            return response.choices[0].message.content.strip()

        except Exception as err:
            return f"An error occurred: {err}"
