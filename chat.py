import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from huggingface_hub import login

# Iniciar sesión en Hugging Face (coloca tu token aquí)
huggingface_token = "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"
login(huggingface_token)

# Cargar el modelo Llama 2 y su tokenizer desde Hugging Face
model_name = "TheBloke/Llama-2-13B-chat-GPTQ"  
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

# Crear la aplicación en Streamlit
st.title('Chatbot con Llama 2 utilizando Hugging Face')
input_text = st.text_input("Haz tu pregunta:")

# Función para generar la respuesta
def generate_response(question):
    inputs = tokenizer(question, return_tensors="pt").to("cuda")  # Si tienes GPU, usa "cuda"
    outputs = model.generate(**inputs, max_length=512, do_sample=True, temperature=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Invocar el modelo y mostrar la respuesta en Streamlit
if input_text:
    with st.spinner("Generando respuesta..."):
        response = generate_response(input_text)
        st.write(response)
