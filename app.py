from fastapi import (
    FastAPI,
    HTTPException,
)  # Importa FastAPI para crear la API y HTTPException para manejar errores
from fastapi.responses import (
    JSONResponse,
)  # Permite enviar respuestas JSON personalizadas
import uvicorn  # Servidor ASGI para ejecutar la aplicación FastAPI
import requests  # Librería para hacer solicitudes HTTP
from dotenv import load_dotenv  # Carga variables de entorno desde un archivo .env
import os  # Permite acceder a las variables de entorno
import json  # Permite trabajar con datos en formato JSON

# Carga las variables de entorno definidas en el archivo .env
load_dotenv()

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

# Obtiene el modelo seleccionado y la URL de Ollama desde las variables de entorno
selected_model = os.getenv("SELECTED_MODEL", "llama3.2")
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")


@app.get("/get_models")
def get_models():
    try:
        # Hacer una solicitud GET para obtener los modelos disponibles en Ollama
        response = requests.get(f"{ollama_url}/models/list")

        if response.status_code == 200:
            # Suponiendo que la respuesta es una lista de modelos en formato JSON
            models = response.json()
            return {"models": models}
        else:
            return JSONResponse(
                content={"status": "Failed to retrieve models", "error": response.text},
                status_code=response.status_code,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set_model")
def set_model(model_name: str):  # Endpoint para seleccionar el modelo de Ollama
    global selected_model
    try:
        # Envía una solicitud para cargar el modelo en Ollama
        response = requests.post(
            f"{ollama_url}/models/load", json={"model": model_name}
        )
        if response.status_code == 200:
            selected_model = model_name  # Actualiza el modelo seleccionado
            return JSONResponse(
                content={"status": "Model selected successfully", "model": model_name},
                status_code=200,
            )
        else:
            return JSONResponse(
                content={"status": "Failed to load model", "error": response.text},
                status_code=response.status_code,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import re  # Para manejar espacios extra


@app.post("/generate_response/")
async def generate_response(prompt: str):
    url = f"{ollama_url}/api/generate"
    payload = {"model": selected_model, "prompt": prompt}

    try:
        response = requests.post(
            url, json=payload, headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        # Acumular los fragmentos de respuesta
        fragments = []
        for line in response.text.strip().split("\n"):
            if line:
                try:
                    data = json.loads(line)
                    fragments.append(data.get("response", ""))
                except json.JSONDecodeError:
                    continue  # Ignorar líneas no JSON

        # Unir fragmentos sin espacios innecesarios
        llama_response = "".join(fragments)

        # Limpiar espacios incorrectos entre letras y signos de puntuación
        cleaned_response = re.sub(r"\s+", " ", llama_response)  # Quita espacios dobles
        cleaned_response = re.sub(
            r"\s([?.!,¿])", r"\1", cleaned_response
        )  # Elimina espacio antes de signos
        cleaned_response = re.sub(
            r"([¿¡])\s", r"\1", cleaned_response
        )  # Elimina espacio después de ¿ o ¡

        return {"response": cleaned_response.strip()}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {e}")


# Punto de entrada para ejecutar el servidor usando uvicorn
import subprocess  # Permite ejecutar comandos del sistema


def run_streamlit():
    try:
        # Ejecuta el script de Streamlit ubicado en main.py
        subprocess.run(["streamlit", "run", "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar Streamlit: {e}")


if __name__ == "__main__":
    run_streamlit()
    uvicorn.run(app, host="0.0.0.0", port=8000)
