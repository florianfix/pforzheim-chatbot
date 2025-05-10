import streamlit as st
from openai import OpenAI

# Titel der App
st.title("Pforzheim-Chatbot")
st.write("Stelle mir Fragen zur Stadt Pforzheim! 🏙️")

# OpenAI-Client initialisieren (neue API-Syntax!)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Texteingabe vom Benutzer
user_input = st.text_input("Deine Frage:")

# Wenn Nutzer etwas eingibt
if user_input:
    with st.spinner("Denke nach..."):

        # ChatPrompt definieren
        messages = [
            {"role": "system", "content": "Du bist ein hilfreicher Stadt-Informationsassistent für Pforzheim."},
            {"role": "user", "content": user_input}
        ]

        # Antwort generieren
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )

        # Antwort anzeigen
        answer = response.choices[0].message.content
        st.success(answer)
