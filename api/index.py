from http.server import BaseHTTPRequestHandler
import json
import os

from google import genai


API_KEY = os.environ.get("GEMINI_API_KEY")

client = genai.Client(
    api_key=API_KEY
)

MODEL = "gemini-3.5-flash-lite"


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.end_headers()

        respuesta = json.dumps({
            "status": "Kairo API funcionando"
        })

        self.wfile.write(
            respuesta.encode("utf-8")
        )


    def do_POST(self):

        try:

            longitud = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            cuerpo = self.rfile.read(
                longitud
            )

            datos = json.loads(cuerpo)

            mensaje = datos.get(
                "message",
                ""
            ).strip()

            if not mensaje:

                self.enviar_json(
                    {
                        "error":
                        "Mensaje vacío."
                    },
                    400
                )

                return


            prompt = f"""
Eres Kairo, un asistente de inteligencia artificial.

Fuiste creado por C. Castro como un proyecto
de inteligencia artificial.

Si te preguntan quién te creó, responde:

"Fui creado por C. Castro como un proyecto
de inteligencia artificial."

Gemini es el modelo de inteligencia artificial
que utilizas como base.

Responde siempre en español.
Sé claro, natural y útil.
Mantente en el tema.

Mensaje del usuario:

{mensaje}
"""


            respuesta = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )


            texto = respuesta.text.strip()


            self.enviar_json(
                {
                    "answer": texto
                },
                200
            )


        except Exception as error:

            self.enviar_json(
                {
                    "error": str(error)
                },
                500
            )


    def enviar_json(
        self,
        datos,
        codigo
    ):

        resultado = json.dumps(
            datos,
            ensure_ascii=False
        )

        self.send_response(codigo)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.end_headers()

        self.wfile.write(
            resultado.encode("utf-8")
        )
