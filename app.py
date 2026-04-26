import streamlit as st
from huggingface_hub import InferenceClient

# 1. Jouw persoonlijke instellingen
TOKEN = "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"
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"
client = InferenceClient(MODEL_ID, token=TOKEN)

st.set_page_config(page_title="Mijn Talkie Kloon", page_icon="🤖")
st.title("🤖 Mijn AI Character")
st.caption("Gratis en zonder advertenties")

# 2. Geef je karakter een persoonlijkheid (zoals in Talkie)
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "Je bent een vriendelijke, behulpzame AI met een eigen persoonlijkheid. Je praat in het Nederlands."

# 3. Chat geschiedenis bijhouden
if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. De chat interactie
if prompt := st.chat_input("Zeg iets tegen je AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # We sturen de persoonlijkheid en de chat mee naar de AI
        messages_to_send = [{"role": "system", "content": st.session_state.system_prompt}]
        messages_to_send.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages])
        
        response = client.chat_completion(
            messages=messages_to_send,
            max_tokens=500,
        )
        
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
