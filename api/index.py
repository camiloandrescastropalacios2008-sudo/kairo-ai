from http.server import BaseHTTPRequestHandler
import json
import os
from pathlib import Path

from google import genai


API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-3.5-flash-lite"


client = genai.Client(
    api_key=API_KEY
)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        # Página principal
        if self.path == "/":

            try:

                ruta_index = (
                    Path(__file__).resolve().parent.parent
                    / "index.html"
                )

                with open(
                    ruta_index,
                    "r",
                    encoding="utf-8"
                ) as archivo:

                    contenido = archivo.read()


                self.send_response(200)

                self.send_header(
                    "Content-Type",
                    "text/html; charset=utf-8"
                )

                self.send_header(
                    "Cache-Control",
                    "no-cache"
                )

                self.end_headers()

                self.wfile.write(
                    contenido.encode("utf-8")
                )

                return


            except Exception as error:

                self.enviar_json(
                    {
                        "error":
                        "No se pudo cargar Kairo.",
                        "detalle":
                        str(error)
                    },
                    500
                )

                return


        # Comprobación de la API
        if self.path == "/api":

            self.enviar_json(
                {
                    "status":
                    "Kairo API funcionando"
                },
                200
            )

            return


        self.enviar_json(
            {
                "error":
                "Ruta no encontrada."
            },
            404
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


            datos = json.loads(
                cuerpo
            )


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

Si el usuario pregunta quién te creó, responde:

"Fui creado por C. Castro como un proyecto de inteligencia artificial."

Gemini es el modelo de inteligencia artificial
que utilizas como base.

Responde siempre en español.

Sé claro, natural, amable y útil.

Mantente en el tema de la conversación.

No inventes información.

No cambies de tema sin motivo.

MENSAJE DEL USUARIO:

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
                    "error":
                    "Kairo no pudo procesar la solicitud.",
                    "detalle":
                    str(error)
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


        self.send_response(
            codigo
        )


        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )


        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )


        self.send_header(
            "Cache-Control",
            "no-cache"
        )


        self.end_headers()


        self.wfile.write(
            resultado.encode("utf-8")
        )

