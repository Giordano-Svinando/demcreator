import streamlit as st
from openai import OpenAI

# Configurazione Segreti (l'app leggerà la chiave dalle impostazioni di Streamlit)
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = None

client = OpenAI(api_key=api_key)

st.set_page_config(page_title="AI Email Generator", layout="centered")

st.title("📧 Email Copy Generator")
st.info("Strumento interno per la generazione di copy promozionali multilingua.")

# Menu Selezione Lingua
lingua = st.selectbox("In quale lingua vuoi i testi?", 
                      ["Italiano", "Tedesco", "Francese", "Inglese Britannico", "Olandese"])

# Input Campi
offerta = st.text_area("1. Descrizione Offerta Commerciale (es. Prodotto, Prezzo, Sconto)", height=100)
concept = st.text_area("2. Tema / Concept Creativo (es. Vibes estive, Black Friday, San Valentino)", height=100)
shipping = st.checkbox("Menziona Spedizione Gratuita")

if st.button("Genera Copy Ora", type="primary"):
    if not api_key:
        st.error("Errore: API Key non configurata nei Secrets di Streamlit.")
    elif not offerta or not concept:
        st.warning("Assicurati di inserire sia l'offerta che il concept.")
    else:
        with st.spinner('Lavoro in corso...'):
            prompt = f"""
            Genera un copy per un'email promozionale in lingua {lingua}.
            OFFERTA: {offerta}
            CONCEPT: {concept}
            NOTE: {f'Includi spedizione gratuita' if shipping else ''}

            Formatta il risultato così:
            - **Oggetto**: [Prodotto + Prezzo esatto] + [Accenno al tema]
            - **Preview**: [Argomentazione del tema] + [Spedizione gratuita se prevista]
            - **Oggetto Reminder**: [Focus sul tema]
            - **Preview Reminder**: [Focus sull'offerta]
            - **Body**: [Max 70 parole. Emozionale, tematizzato, non ripetere dati tecnici dell'offerta]
            - **CTA**: [Pushy e in tema]
            - **CTA Reminder**: [Alternativa]
            """
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            st.success("Generazione completata!")
            st.markdown("---")
            st.markdown(response.choices[0].message.content)

import time
from openai import RateLimitError

def call_with_retry(client, **kwargs):
    wait = 1
    for _ in range(6):
        try:
            return client.chat.completions.create(**kwargs)
        except RateLimitError:
            time.sleep(wait)
            wait *= 2
    raise

