import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
from gtts import gTTS
from googletrans import Translator

st.set_page_config(page_title="Traductor Mágico 🎧🌍", page_icon="🌐")

st.markdown(
    """
    <style>
        html, body, .stApp {
            background-color: #00cccc !important;
        }
        h1, h2, h3, h4, p {
            text-align: center;
            color: #00796b;
            font-family: 'Comic Sans MS', cursive;
        }
        .stButton>button {
            background-color: #4dd0e1;
            color: #ffffff;
            border-radius: 10px;
            padding: 10px 20px;
            display: block;
            margin: auto;
        }
        .stSelectbox, .stTextInput, .stTextArea, .stCheckbox {
            text-align: center;
            margin: auto;
        }
        .block-container {
            display: flex;
            justify-content: center;
        }
        .stImage {
            display: flex;
            justify-content: center;
        }
        .stAudio {
            display: flex;
            justify-content: center;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1>🌐 Traductor Mágico 🎧</h1>', unsafe_allow_html=True)
st.markdown('<h3>🎙️ Habla y nosotros lo traducimos con amor 💌</h3>', unsafe_allow_html=True)

image = Image.open('lenguas.jpg')
st.image(image, width=700)

st.markdown("""
<div style="background-color:#ffffffcc; padding: 15px; border-radius: 12px; margin-bottom: 20px;">
  <h4>✨ ¡Bienvenida, viajera de las palabras! ✨</h4>
  <p>Yo soy tu traductor mágico 💫. Aquí puedes hablar, y yo traduciré lo que dices al idioma que necesites 🌍.</p>
  <p>Ideal para practicar idiomas, traducir ideas secretas o simplemente escuchar tu voz en otro idioma 🎧.</p>
  <p>¿Lista para empezar? 💬 ¡Hablemos!</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.subheader("🔊 Cómo usar el Traductor:")
    st.write("1️⃣ Presiona el botón de 'Escuchar 🎤'.")
    st.write("2️⃣ Habla claramente lo que deseas traducir.")
    st.write("3️⃣ Elige los idiomas y convierte a audio.")
    st.write("¡Es magia lingüística al instante! ✨")

st.markdown("<h4>🎤 Toca el botón y habla lo que quieras traducir:</h4>", unsafe_allow_html=True)

stt_button = Button(label="🎤 Escuchar", width=300, height=50)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

if result:
    if "GET_TEXT" in result:
        st.markdown("<h4>🎧 Lo que dijiste:</h4>", unsafe_allow_html=True)
        st.write(result.get("GET_TEXT"))

    try:
        os.mkdir("temp")
    except:
        pass

    st.markdown("<h3>🎼 Traducción y conversión a audio</h3>", unsafe_allow_html=True)

    translator = Translator()
    text = str(result.get("GET_TEXT"))

    in_lang = st.selectbox("🌍 Selecciona el idioma de entrada:",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"))

    if in_lang == "Inglés":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "Coreano":
        input_language = "ko"
    elif in_lang == "Mandarín":
        input_language = "zh-cn"
    elif in_lang == "Japonés":
        input_language = "ja"

    out_lang = st.selectbox("🗣️ Selecciona el idioma de salida:",
        ("Inglés", "Español", "Bengali", "Coreano", "Mandarín", "Japonés"))

    if out_lang == "Inglés":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "Coreano":
        output_language = "ko"
    elif out_lang == "Mandarín":
        output_language = "zh-cn"
    elif out_lang == "Japonés":
        output_language = "ja"

    english_accent = st.selectbox("🎧 Acento del audio:",
        ("Defecto", "Español", "Reino Unido", "Estados Unidos", "Canada", "Australia", "Irlanda", "Sudáfrica"))

    if english_accent == "Defecto":
        tld = "com"
    elif english_accent == "Español":
        tld = "com.mx"
    elif english_accent == "Reino Unido":
        tld = "co.uk"
    elif english_accent == "Estados Unidos":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Irlanda":
        tld = "ie"
    elif english_accent == "Sudáfrica":
        tld = "co.za"

    def text_to_speech(input_language, output_language, text, tld):
        translation = translator.translate(text, src=input_language, dest=output_language)
        trans_text = translation.text
        tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
        try:
            my_file_name = text[0:20]
        except:
            my_file_name = "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name, trans_text

    display_output_text = st.checkbox("📄 Mostrar texto traducido")

    if st.button("🎧 Convertir y escuchar"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown("🔊 **Tu audio está listo:**")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown("📝 **Texto traducido:**")
            st.write(output_text)

    def remove_files(n):
        mp3_files = glob.glob("temp/*mp3")
        if len(mp3_files) != 0:
            now = time.time()
            n_days = n * 86400
            for f in mp3_files:
                if os.stat(f).st_mtime < now - n_days:
                    os.remove(f)

    remove_files(7)
