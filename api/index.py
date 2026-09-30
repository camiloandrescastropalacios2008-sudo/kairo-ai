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

        # Mostrar la página principal
        if self.path == "/":

            try:

                with open(
                    "index.html",
                    "r",
                    encoding="utf-8"
                ) as archivo:

                    contenido = archivo.read()


                self.send_response(200)

                self.send_header(
                    "Content-Type",
                    "text/html; charset=utf-8"
                )

                self.end_headers()

                self.wfile.write(
                    contenido.encode("utf-8")
                )

            except Exception as error:

                self

