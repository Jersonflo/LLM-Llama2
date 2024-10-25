import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder, ChatPromptTemplate
import torch
import os
import subprocess



model_path = "/Users/mareo/Desktop/LLM-Llama2/llama_model/Llama-3.1-8B-Lexi-Uncensored_V2_Q5.gguf"
    

# Función para generar respuestas usando llama.cpp
def generate_response(prompt):
    try:
        # Ejecuta llama.cpp con el prompt como entrada
        result = subprocess.run(
            ['./llama.cpp/llama-cli', '-m', model_path, '-p', prompt, '--n_predict', '128'],
            capture_output=True,
            text=True
        )
        # Retorna la salida generada por el modelo
        return result.stdout.strip()
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
        return ""

# Función para manejar la entrada del usuario
def submit_message():
  if st.session_state["user_input"]:
        try:
            prompt = st.session_state["bot_description"] + "\n" + st.session_state["user_input"]
            response = generate_response(prompt)

            # Añadir los mensajes al historial
            st.session_state["chat_history"].append(HumanMessage(content=st.session_state["user_input"]))
            st.session_state["chat_history"].append(AIMessage(content=response))

            # Limpiar la entrada del usuario
            st.session_state["user_input"] = ""
            update_conversation_text()
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")

# Función para borrar el historial del chat
def clear_chat_history():
    st.session_state["chat_history"] = []
    st.session_state["conversation_text"] = ""


def update_conversation_text():
    conversation = ""
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            conversation += f"🧑 Usuario: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            conversation += f"🤖 Asistente: {msg.content}\n"
    st.session_state["conversation_text"] = conversation


def main():
  
   # Cambiar el color de fondo de toda la página
    st.markdown(
        """
        <style>
        /* Aplica el color de fondo a todo el body, html y otras clases necesarias */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background-color: #03051A;  /* Cambia este valor por el color de fondo que desees */
        }

           /* Cambiar el color de fondo del sidebar */
        [data-testid="stSidebar"] {
            background-color: #291947;  /* Color de fondo del sidebar */
        }

        /* Estilo del título */
        h1 {
            text-align: center;
            color: white;
            padding-top: 20px; /* Aseguramos que esté separado del contenido superior */
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

        # Inicializar variables de sesión
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []
    if "conversation_text" not in st.session_state:
        st.session_state["conversation_text"] = ""
    if "bot_description" not in st.session_state:
        st.session_state["bot_description"] = (
            "Eres un asistente virtual llamado Juan. "
            "Respondes preguntas de manera sencilla y haces preguntas básicas para conocer al usuario."
        )

    
   # Cargar la imagen desde el directorio local
    image_path = os.path.expanduser("~/Desktop/LLM-Llama2/image.png")
    st.image(image_path, caption="Ecosystem Tech Chatbot", use_column_width=True)

    # Mostrar tutorial/instrucción inicial solo una vez
    if "tutorial_visto" not in st.session_state:
        st.info("Bienvenido al chatbot. Escribe una pregunta o selecciona un tono de respuesta para comenzar.")
        st.session_state["tutorial_visto"] = True

       # Configuración de la barra lateral
    with st.sidebar:
        bot_name = st.text_input("Nombre del Asistente Virtual:", value="Juan")
        tone = st.selectbox("Selecciona el tono del asistente:", ["Formal", "Casual", "Humorístico", "Técnico"])
        st.session_state["bot_description"] = (
            f"Eres un asistente virtual llamado {bot_name}. "
            f"Respondes de manera {tone.lower()} y haces preguntas básicas para conocer al usuario."
        )

        # Botón para borrar el historial del chat   
        if st.button("Borrar historial del chat"):
            clear_chat_history()
            

    # Mostrar el área de texto con la conversación completa
    st.text_area("Historial de conversación", value=st.session_state["conversation_text"], height=300, disabled=True)

    # Estilos personalizados para los mensajes del usuario y del bot
    st.markdown(
        """
        <style> 

        .user-message {
            background-color: #03051A;
            border-radius: 10px;
            padding: 8px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 70%;
            word-wrap: break-word;
            text-align: left;
            color: #FFFFFF;
        }
        
        .assistant-message {
            background-color: #03051A;
            border-radius: 10px;
            padding: 8px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 90%;
            word-wrap: break-word;
            text-align: left;
            color: #FFFFFF;
        }

        .block-container {
            padding-top: 20px;
            padding-bottom: 10px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            height: 90vh;
        }

        div.stButton > button {
            background-color: #B099DB;
            color: white;
            border-radius: 15px;
            padding: 10px 20px;
            border-color: #49DDC0;
        }

         /* Cambia el borde y el color al pasar el cursor sobre los inputs de texto, selectbox y text_area */
        .stTextInput input:hover, .stTextArea textarea:hover, .stSelectbox div:hover {
            border-color: #49DDC0 !important; 
        }

        /* Cambia el borde y color cuando un elemento está seleccionado o enfocado */
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox div:focus {
            border-color: #49DDC0 !important;  /* Cambia el color del borde al seleccionar el elemento */
            outline: none !important;  /* Elimina el borde rojo que aparece por defecto */
            box-shadow: 0 0 5px rgba(73, 221, 192, 0.7);  /* Añade un resplandor alrededor del borde */
        }

  

        </style>
        """, 
        unsafe_allow_html=True
    )

    
    # Casilla de entrada con on_change para manejar el evento de envío
    st.text_input("¿Qué deseas saber?:", key="user_input", on_change=submit_message)
    st.info("Presiona Enter para enviar tu mensaje.")


if __name__ == '__main__':
    main()
