import requests
from flask import current_app


class AIServiceError(Exception):
    pass


class AIService:
    def _system_mesaji(self):
        return current_app.config["BUSINESS_CONTEXT"]

    def _groq_istegi(self, mesaj, gecmis=None):
        api_key = current_app.config["GROQ_API_KEY"]

        if not api_key:
            return "Demo modu aktif. Yapay zekâ API anahtarı henüz eklenmedi."

        messages = [
            {
                "role": "system",
                "content": self._system_mesaji()
            }
        ]

        if gecmis:
            messages.extend(gecmis)

        messages.append(
            {
                "role": "user",
                "content": mesaj
            }
        )

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": messages
                },
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            return data["choices"][0]["message"]["content"]

        except requests.RequestException as e:
            print("GROQ HATASI:", e)

            if hasattr(e, "response") and e.response is not None:
                print("STATUS:", e.response.status_code)
                print("CEVAP:", e.response.text)

            raise AIServiceError(
                "Yapay zekâ servisine bağlanırken bir hata oluştu."
            ) from e

    def yanit_uret(self, mesaj, gecmis=None):
        return self._groq_istegi(mesaj, gecmis)


ai_service = AIService()