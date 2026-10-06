import random
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator


words_by_level = {
    "facil":[
        "perro",
        "casa",
        "sol",
        "luna",
        "gato",
        "agua",
        "leche",
        "pan",
        "libro",
        "mesa",
        "silla",
        "puerta",
        "escuela",
        "amigo",
        "familia",
        "comida",
        "manzana",
        "banana",
        "rojo",
        "azul"
    ],

    "medio": [
        "ventana",
        "amarillo",
        "hermano",
        "hermana",
        "jardin",
        "ciudad",
        "playa",
        "montaña",
        "pelota",
        "bicicleta",
        "telefono",
        "computadora",
        "profesor",
        "estudiante",
        "animales",
        "desayuno",
        "domingo",
        "invierno",
        "verano",
        "familia"
    ],

    "dificil": [
        "tecnologia",
        "universidad",
        "informacion",
        "pronunciacion",
        "imaginacion",
        "educacion",
        "responsabilidad",
        "conocimiento",
        "medioambiente",
        "comunicacion",
        "experiencia",
        "oportunidad",
        "desarrollo",
        "investigacion",
        "creatividad",
        "importante",
        "diferente",
        "internacional",
        "organizacion",
        "sostenibilidad"
    ]
}

#hola

duration = 5  # segundos de grabación
sample_rate = 44100

point = 0
errors = 0

translator = Translator() 
recognizer = sr.Recognizer()

print("Este es un programa que te ayuda a mejorar tus habilidades con el ingles, te va a mostrar una palabra y solo tiene 3 intentos para traducirla.")
print("Selecciona una dificultad:")
print("Fácil")
print("Medio")
print("Difícil")

level = input("Escribe facil, medio o dificil: ")

while level not in ["facil", "medio", "dificil"]:
    print("Opción no válida.")
    level = input("Escribe facil, medio o dificil: ")


print("Que comience.....")



while errors < 3:

    word_to_say = random.choice(words_by_level[level])
    print(word_to_say)
    translated = translator.translate(
        word_to_say,
        src="es",
        dest="en"
    )

    correct_answer = translated.text.lower().strip()

    print("Habla ahora...")

    recording = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16"
    )

    sd.wait()

    wav.write("output.wav", sample_rate, recording)
    print("Grabación completa, ahora reconociendo...")

    recognizer = sr.Recognizer()

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)

    try:

        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        print("Dijiste:", text)

        text = text.lower().strip()

        if text == correct_answer:

            point = point + 1

            print("Correcto.")
            print("Puntos:", point)

        else:

            errors = errors + 1

            print("Incorrecto.")
            print("En realidad es:", correct_answer)
            print("Errores:", errors)

    except sr.UnknownValueError:

        errors = errors + 1

        print("No esta claro")
        print("Errores:", errors)

    except sr.RequestError as e:

        print(f"Error del servicio: {e}")


print("Gracias por jugar:)")
print("Puntos:", point)
print("Errores:", errors)

