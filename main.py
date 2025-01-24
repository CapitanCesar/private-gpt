import streamlit as st
import requests
from dotenv import load_dotenv  # Carga variables de entorno desde un archivo .env
import os  # Permite acceder a las variables de entorno
import json  # Permite trabajar con datos en formato JSON

# Carga las variables de entorno definidas en el archivo .env
load_dotenv()

# URL del servicio del bot
selected_model = os.getenv("SELECTED_MODEL", "llama3.2")
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")

# Configuración de la página
st.set_page_config(page_title="Chatbot con Streamlit", page_icon="🤖")

# Título de la aplicación
st.title("💬 Chatbot con Streamlit")

# Inicializar el historial de conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Mostrar el mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Realizar la petición al bot
    url = f"{ollama_url}/api/generate"
    payload = {"model": selected_model, "prompt": user_input}

    try:
        response = requests.post(
            url, json=payload, headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        llama_response = ""
        # Procesa cada línea de la respuesta
        for line in response.text.strip().split("\n"):
            if line:
                try:
                    data = json.loads(line)
                    llama_response += data.get("response", "")
                except json.JSONDecodeError:
                    continue  # Ignora líneas no JSON

        bot_reply = llama_response.strip()
    except Exception as e:
        bot_reply = f"Error al conectar con el servidor: {e}"

    # Mostrar la respuesta del bot
    st.session_state.messages.append({"role": "ai", "content": bot_reply})
    with st.chat_message("ai"):
        st.markdown(bot_reply)
