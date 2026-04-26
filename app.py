import streamlit as st
from huggingface_hub import InferenceClient

# We halen het token veilig uit de 'Secrets' kluis van Streamlit
try:
    TOKEN = st.secrets["HF_TOKEN"]
except:
    st.error("Oeps! Je moet je token nog in de 'Secrets' van Streamlit zetten.")
    st.stop()

# Dit model is erg goed en meestal online
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"
client = InferenceClient(MODEL_ID, token=TOKEN)

st.set_page_config(page_title="Mijn Eigen Talkie", page_icon="🤖")
st.title("🤖 Mijn AI Character")
st.caption("Gratis, veilig en zonder advertenties")

# Chat geschiedenis instellen
if "messages" not in st.session_state:
    st.session_state.messages = []

# Toon alle berichten in de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input van de gebruiker
if prompt := st.chat_input("Typ je bericht..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI antwoord genereren
    try:
        with st.chat_message("assistant"):
            response = ""
            # We laten de tekst 'streamen' (letter voor letter typen) voor het Talkie-gevoel
            for message in client.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                stream=True,
            ):
                token_text = message.choices.delta.content
                if token_text:
                    response += token_text
            
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error("De AI wordt wakker... Probeer het over 10 seconden nog eens!")
