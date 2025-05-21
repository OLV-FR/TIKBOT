
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import requests
import zipfile

# Paramètres du modèle
MODEL_NAME = "vosk-model-small-fr-0.22"
MODEL_URL = f"https://alphacephei.com/vosk/models/{MODEL_NAME}.zip"

# Fonction pour télécharger le modèle Vosk si absent
def download_vosk_model():
    if not os.path.exists(MODEL_NAME):
        print(f"Le modèle {MODEL_NAME} est introuvable. Téléchargement en cours...")
        zip_path = f"{MODEL_NAME}.zip"

        try:
            with requests.get(MODEL_URL, stream=True) as r:
                r.raise_for_status()
                with open(zip_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

            print("Téléchargement terminé. Extraction du modèle...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            os.remove(zip_path)
            print("Modèle prêt à l'emploi.")
        except Exception as e:
            print(f"Erreur lors du téléchargement du modèle : {e}")
            sys.exit(1)
    else:
        print("Modèle Vosk déjà présent.")

# Télécharger et charger le modèle
download_vosk_model()
model = vosk.Model(MODEL_NAME)

# Configuration de l'entrée audio
samplerate = 16000
device = None  # Peut être changé si nécessaire

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

def main():
    print("Parlez dans votre micro. Appuyez sur Ctrl+C pour quitter.")
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                           dtype='int16', channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)

        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    print("Vous avez dit :", result.get("text", ""))
                else:
                    partial = json.loads(rec.PartialResult())
                    print("Reconnaissance partielle :", partial.get("partial", ""))
        except KeyboardInterrupt:
            print("\nArrêt du programme.")

if __name__ == "__main__":
    main()
