import streamlit as st
from huggingface_hub import InferenceClient

# Hier halen we het token nu VEILIG op uit de kluis
TOKEN = st.secrets["HF_TOKEN"]
MODEL_ID = "HuggingFaceH4/zephyr-7b-beta"

client = InferenceClient(MODEL_ID, token=TOKEN)

st.set_page_config(page_title="Mijn Talkie", page_icon="🤖")
st.title("🤖 Mijn AI Character")

# ... (de rest van de code blijft hetzelfde als de vorige keer)
