import streamlit as st
import openai
import time
from openai import RateLimitError, AuthenticationError, APIConnectionError, APIError

# API-Key aus Streamlit Secrets laden
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.title("💬 Pforzheim Chatbot")
user_input = st.text_input("Frage zur Stadt Pforzheim:")

if user_input:
    with st.spinner("Antwort wird geladen..."):
        messages = [
            {"role": "system", "content": "Du bist ein hilfreicher Chatbot mit Informationen über die Stadt Pforzheim."},
            {"role": "user", "content": user_input},
        ]

        # Fehlerbehandlung mit Retry (max. 3 Versuche)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.5,
                )
                reply = response.choices[0].message.content
                st.success(reply)
                break  # Erfolgreich -> Schleife beenden

            except RateLimitError:
                st.warning("⚠️ Zu viele Anfragen. Warte 10 Sekunden...")
                time.sleep(10)  # Wartezeit vor erneutem Versuch

            except AuthenticationError:
                st.error("🚫 Ungültiger API-Key. Bitte überprüfe deine Einstellungen.")
                break

            except APIConnectionError:
                st.error("🔌 Verbindungsfehler zu OpenAI. Prüfe deine Internetverbindung.")
                break

            except APIError:
                st.error("❗ Interner Fehler bei OpenAI. Bitte versuche es später erneut.")
                break

        else:
            st.error("⏱️ Anfrage fehlgeschlagen nach mehreren Versuchen. Bitte später erneut versuchen.")

