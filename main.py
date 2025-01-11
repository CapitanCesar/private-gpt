from fastapi import FastAPI, HTTPException  # Importa FastAPI para crear la API y HTTPException para manejar errores
from fastapi.responses import JSONResponse  # Permite enviar respuestas JSON personalizadas
import uvicorn  # Servidor ASGI para ejecutar la aplicación FastAPI
import requests  # Librería para hacer solicitudes HTTP

# Crea una instancia de la aplicación FastAPI
app = FastAPI()

@app.post("/send_message")
def send_message(message: str):  # Define un endpoint POST que recibe un mensaje de tipo string
    try:
        # Envía una solicitud POST al servidor de Ollama en local con el mensaje recibido
        response = requests.post("http://localhost:11434/send", json={"message": message})
        
        # Si la respuesta es exitosa (código 200), devuelve un JSON indicando éxito
        if response.status_code == 200:
            return JSONResponse(
                content={"status": "Message sent successfully", "response": response.json()},  # Respuesta con el contenido recibido
                status_code=200
            )
        else:
            # Si ocurre un error, devuelve el mensaje de error y el código de estado recibido
            return JSONResponse(
                content={"status": "Failed to send message", "error": response.text},
                status_code=response.status_code
            )
    except Exception as e:
        # Captura cualquier excepción inesperada y devuelve un error 500
        raise HTTPException(status_code=500, detail=str(e))

# Punto de entrada para ejecutar el servidor usando uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Ejecuta la aplicación en todas las interfaces de red, puerto 8000
