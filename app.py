import streamlit as st
from huggingface_hub import InferenceClient


try:
    TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("Stap nog niet klaar: Zet je token in de 'Secrets' van Streamlit Cloud!")
    st.stop()

MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"
client = InferenceClient(MODEL_ID, token=TOKEN)

st.title("🤖 Mijn Eigen Talkie")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Typ je bericht..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # De AI aanroepen
            response = client.text_generation(prompt, max_new_tokens=500)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error("De AI start op... probeer het over 10 seconden nog eens!")
