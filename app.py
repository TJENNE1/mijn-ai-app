import streamlit as st
from huggingface_hub import InferenceClient

# Jouw token (deze blijft hetzelfde)
TOKEN = "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"
# We gebruiken nu een ander model dat stabieler is
MODEL_ID = "meta-llama/Llama-3.2-1B-Instruct"

client = InferenceClient(MODEL_ID, token=TOKEN)

st.set_page_config(page_title="Mijn Talkie", page_icon="🤖")
st.title("🤖 Mijn Eigen Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon geschiedenis
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat invoer
if prompt := st.chat_input("Typ hier iets..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # De AI aanroepen
            response = client.text_generation(
                prompt,
                max_new_tokens=500,
                return_full_text=False
            )
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error("De AI slaapt nog even. Probeer het over 10 seconden nog eens!")
