import os
import speech_recognition as sr
from llama_cpp import Llama
from gtts import gTTS
from playsound import playsound  # Ensure playsound1 is used if needed
from googletrans import Translator
from colorama import Fore, Style

def install_dependencies():
    try:
        print("[SAFE MODE] Installing dependencies...")
        os.system("pip install SpeechRecognition llama-cpp-python gtts playsound1 googletrans colorama")
    except Exception:
        print("[ERROR] Could not install dependencies")
        exit()

log = []

def printlog():
    os.system("clear" if os.name == "posix" else "cls")
    for line in log:
        print(line)

def load_ai_model():
    model_path = "llama-7B.gguf"
    if not os.path.exists(model_path):
        log.append(f"[{Fore.RED}{Style.BRIGHT}ERROR{Fore.WHITE}{Style.NORMAL}] AI model missing, downloading...")
        printlog()
        os.system("wget -O llama-7B.gguf https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf")
    return Llama(model_path=model_path, n_ctx=2048)

def ai(q):
    llm = load_ai_model()
    prompt = f"You are an AI assistant named VenAI. Respond concisely in one line without mentioning the user. Only respond to the first line.\n{q}\n"
    response = llm.create_completion(prompt, max_tokens=50)
    output = response["choices"][0]["text"].strip().splitlines()[0]
    log.append(f"[{Fore.GREEN}{Style.BRIGHT}OK{Fore.WHITE}{Style.NORMAL}] AI CREATED OUTPUT")
    printlog()
    return output

# Initialize recognizer
recognizer = sr.Recognizer()
translator = Translator()

def main():
    running = True
    while running:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... please wait.")
            recognizer.adjust_for_ambient_noise(source)
            print("Say something in Polish!")
            audio = recognizer.listen(source)

        try:
            recognized = recognizer.recognize_google(audio, language="pl-PL")
            log.append(f"[{Fore.GREEN}{Style.BRIGHT}OK{Fore.WHITE}{Style.NORMAL}] Recognized Speech: {recognized}")
            printlog()

            if "Hej" or "hej" in recognized:
                recognized = recognized.replace("Hej Grzegorz", "").strip()
                log.append(f"[{Fore.GREEN}{Style.BRIGHT}OK{Fore.WHITE}{Style.NORMAL}] Approved Input")
                printlog()

                translated_text = translator.translate(recognized, src='pl', dest='en').text
                log.append(f"[{Fore.GREEN}{Style.BRIGHT}OK{Fore.WHITE}{Style.NORMAL}] Translated to English: {translated_text}")
                printlog()

                eng_output = ai(translated_text)
                log.append(f"[{Fore.GREEN}{Style.BRIGHT}OK{Fore.WHITE}{Style.NORMAL}] AI Output: {eng_output}")
                printlog()

                final_output = translator.translate(eng_output, src="en", dest='pl').text
                log.append(f"[{Fore.GREEN}{Style.BRIGHT}OK{Fore.WHITE}{Style.NORMAL}] Translated Back to Polish: {final_output}")
                printlog()

                tts = gTTS(final_output, lang='pl')
                tts.save('output.mp3')
                playsound('output.mp3')
                log.append(f"[{Fore.GREEN}{Style.BRIGHT}OK{Fore.WHITE}{Style.NORMAL}] Played Response")
                printlog()

            else:
                log.append(f"[{Fore.YELLOW}{Style.BRIGHT}WARNING{Fore.WHITE}{Style.NORMAL}] Wake word not detected")
                printlog()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio")
        except sr.RequestError:
            print("There was an error with the speech service")
        except Exception as e:
            print(f"[ERROR] {str(e)}")

        log.clear()    

if __name__ == "__main__":
    main()