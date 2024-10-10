import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatMessagePromptTemplate, MessagesPlaceholder, ChatPromptTemplate

# Inicializa el modelo Llama 
llm = Ollama(model="llama3")

# Función para manejar la entrada del usuario
def submit_message():
    if st.session_state["user_input"]:  # Si el usuario ingresó algo
        response = chain.invoke({
            "input": st.session_state["user_input"],
            "chat_history": st.session_state["chat_history"]
        })
        # Agregar los mensajes al historial
        st.session_state["chat_history"].append(HumanMessage(content=st.session_state["user_input"]))
        st.session_state["chat_history"].append(AIMessage(content=response))
        # Limpiar el input después de enviar el mensaje
        st.session_state["user_input"] = ""  # Restablecer el campo de entrada

          # Actualizar la conversación en el área de texto
        update_conversation_text()


# Función para borrar el historial del chat
def clear_chat_history():
    st.session_state["chat_history"] = []  # Vaciar el historial del chat


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
        
             /* Centrar la imagen */
        .centered-image {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 60%;  /* Ajusta el tamaño de la imagen */
        }

        </style>

        </style>
        """,
        unsafe_allow_html=True
    )

     # Inicializar el área de texto con el historial de chat vacío
    if "conversation_text" not in st.session_state:
        st.session_state["conversation_text"] = ""
    
   # Cargar la imagen desde el directorio local
    st.image("/Users/mareo/Desktop/LLM-Llama2/image.png", caption="Ecosystem Tech Chatbot", use_column_width=True)

    # Mostrar tutorial/instrucción inicial solo una vez
    if "tutorial_visto" not in st.session_state:
        st.info("Bienvenido al chatbot. Escribe una pregunta o selecciona un tono de respuesta para comenzar.")
        st.session_state["tutorial_visto"] = True

    # Crear una barra lateral para el nombre del asistente, la descripción y el botón para borrar el historial
    with st.sidebar:
        bot_name = st.text_input("Nombre del Asistente Virtual:", value="Juan")
        prompt = f"""Eres un asistente virtual te llamas {bot_name}, respondes preguntas con respuestas simples, además debes preguntar al usuario acorde al contexto del chat, también debes preguntarle cosas básicas para conocerlo. Eres un chatbot de la Empresa Ecosystem tech."""
        bot_description = st.text_area("Descripción del asistente virtual:", height=220, value=prompt)

        # Personalización del tono de respuesta
        tone = st.selectbox("Selecciona el tono del asistente:", ["Formal", "Casual", "Humorístico", "Técnico"])
        tone_description = f"Responde de manera {tone.lower()}."  # Ajuste del tono en la respuesta del bot

        # Botón para borrar el historial del chat
        if st.button("Borrar historial del chat"):
            clear_chat_history()

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Ajustar el prompt del chatbot con el tono seleccionado
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", bot_description + " " + tone_description),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    global chain  # Definimos `chain` global para acceder en `submit_message`
    chain = prompt_template | llm

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
        }

         /* Cambia el borde y el color al pasar el cursor sobre los inputs de texto, selectbox y text_area */
        .stTextInput input:hover, .stTextArea textarea:hover, .stSelectbox div:hover {
            border-color: #49DDC0 !important;  /* Cambia el color del borde al pasar el cursor */
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

if __name__ == '__main__':
    main()
