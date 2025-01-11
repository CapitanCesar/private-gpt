# Instalación de Ollama en Windows

## 1. Descargar Ollama

- Visita la página oficial de Ollama:  
  [https://ollama.com/download](https://ollama.com/download)
- Descarga el instalador para Windows.

## 2. Instalar Ollama

- Ejecuta el instalador descargado.
- Sigue las instrucciones del asistente de instalación.

## 3. Iniciar el Servicio de Ollama

- Abre **Símbolo del sistema (CMD)** o **PowerShell**.
- Ejecuta el siguiente comando para iniciar el servicio:
  ```bash
  ollama serve
  ```
- Esto iniciará Ollama en `http://localhost:11434`.

## 4. Verificar que Ollama está activo

- Abre **CMD** o **PowerShell** y ejecuta:
  ```bash
  curl http://localhost:11434
  ```
- Deberías recibir una respuesta indicando que el servicio está en funcionamiento.

## 5. (Opcional) Probar conexión desde FastAPI

- Asegúrate de que tu servidor FastAPI esté corriendo.
- Envía un mensaje de prueba:
  ```bash
  curl -X POST "http://localhost:8000/send_message" -d "message=Hola Ollama"
  ```

¡Listo! Ollama debería estar funcionando correctamente en tu máquina con Windows.

