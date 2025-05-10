import streamlit as st
import openai

# Setze den Titel und das Icon für deine Seite
st.set_page_config(page_title="Pforzheim Chatbot", page_icon="🤖")
st.title("🤖 Pforzheim Chatbot")
st.markdown("Stelle mir Fragen rund um die Stadt Pforzheim!")

# API-Key von OpenAI (über Secrets von Streamlit gespeichert)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Chatverlauf in der Sitzung speichern
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Du bist ein hilfreicher Assistent für die Stadt Pforzheim."}]

# Zeige den bisherigen Chatverlauf
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Eingabefeld für den Benutzer
prompt = st.chat_input("Was möchtest du wissen?")
if prompt:
    # Speichern der Eingabe im Verlauf
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Antwort von OpenAI generieren
    response = openai.ChatCompletion.create(
        model="gpt-4",  # alternativ: gpt-3.5-turbo für weniger Kosten
        messages=st.session_state.messages
    )
    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Antwort anzeigen
    with st.chat_message("assistant"):
        st.markdown(reply)
