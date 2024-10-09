import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatMessagePromptTemplate, MessagesPlaceholder, ChatPromptTemplate

# Inicializa el modelo Llama 
llm = Ollama(model="llama3.1")

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

# Función para borrar el historial del chat
def clear_chat_history():
    st.session_state["chat_history"] = []  # Vaciar el historial del chat

def main():
    # Mantener el título en la parte superior
    st.title("Ecosystem tech Chatbbot llama ")

    # Mostrar tutorial/instrucción inicial solo una vez
    if "tutorial_visto" not in st.session_state:
        st.info("Bienvenido al chatbot. Escribe una pregunta o selecciona un tono de respuesta para comenzar.")
        st.session_state["tutorial_visto"] = True

    # Crear una barra lateral para el nombre del asistente, la descripción y el botón para borrar el historial
    with st.sidebar:
        bot_name = st.text_input("Nombre del Asistente Virtual:", value="Juan")
        prompt = f"""Eres un asistente virtual te llamas {bot_name}, respondes preguntas con respuestas simples, ademas debes preguntar al usuario acorde al contexto del chat, tambien debes preguntarle cosas básicas para conocerlo. Eres un chatbot de la Empresa Ecosystem tech."""
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

    # Estilos personalizados para los mensajes del usuario y del bot
    st.markdown(
        """
        <style>
        .user-message {
            background-color: #e8f4fd;
            border-radius: 10px;
            padding: 8px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 70%;
            word-wrap: break-word;
            text-align: left;
            color: #333;
        }
        .assistant-message {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 8px;
            margin-bottom: 10px;
            width: fit-content;
            max-width: 70%;
            word-wrap: break-word;
            text-align: left;
            color: #333;
        }
        .block-container {
            padding-top: 10px;
            padding-bottom: 10px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            height: 90vh;
        }
        .stTextInput > div > div > input {
            border: 1px solid #ccc;
            border-radius: 15px;
            padding: 10px;
            width: 90%;
            margin: 10px auto;
        }
        div.stButton > button {
            background-color: #ff4b4b;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )

    # Muestra el chat de historial con estilos personalizados
    for msg in st.session_state["chat_history"]:
        if isinstance(msg, HumanMessage):
            st.markdown(f'<div class="user-message">{msg.content}</div>', unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f'<div class="assistant-message">🤖 {bot_name}: {msg.content}</div>', unsafe_allow_html=True)

    # Casilla de entrada con on_change para manejar el evento de envío
    st.text_input("Escribe tu pregunta:", key="user_input", on_change=submit_message)

if __name__ == '__main__':
    main()
