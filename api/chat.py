from http.server import BaseHTTPRequestHandler
import json
import os
from google import genai

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

MODEL = "gemini-3.5-flash-lite"


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        length = int(
            self.headers.get("Content-Length", 0)
        )

        body = self.rfile.read(length)

        data = json.loads(body)

        message = data.get("message", "")

        prompt = f"""
Eres Kairo, un asistente de inteligencia artificial.

Fuiste creado por C. Castro como un proyecto
de inteligencia artificial.

Si te preguntan quién te creó, responde que
fuiste creado por C. Castro.

Gemini es el modelo de inteligencia artificial
que utilizas como base.

Responde en español.
Sé claro, natural y útil.
Mantente en el tema.

Mensaje del usuario:
{message}
"""

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        answer = response.text.strip()

        result = json.dumps({
            "answer": answer
        })

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.end_headers()

        self.wfile.write(
            result.encode("utf-8")
        )
