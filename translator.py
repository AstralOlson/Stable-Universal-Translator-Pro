import os
import sys
import io
import time
import contextlib
import subprocess
import shutil
from datetime import datetime

# --- SILENCE STARTUP NOISE ---
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

def clear_terminal():
    os.system('clear')

@contextlib.contextmanager
def deep_muzzle():
    """Traps hardware errors to keep the screen clean."""
    stderr_fd = sys.stderr.fileno()
    with os.fdopen(os.dup(stderr_fd), 'w') as old_stderr:
        with open(os.devnull, 'w') as devnull:
            sys.stderr.flush()
            os.dup2(devnull.fileno(), stderr_fd)
            try:
                yield
            finally:
                sys.stderr.flush()
                os.dup2(old_stderr.fileno(), stderr_fd)

# Initialize libraries silently
with deep_muzzle():
    import pygame
    import speech_recognition as sr
    from googletrans import Translator, LANGUAGES
    from gtts import gTTS
    pygame.mixer.init()

# --- LOGGING & MAINTENANCE ---

LOG_DIR = os.path.expanduser("~/Desktop/Translator_Logs")

def save_log(original, translated, target_lang):
    """Saves session to the log folder on Desktop."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Translation_{timestamp}.txt"
    filepath = os.path.join(LOG_DIR, filename)
    with open(filepath, "w") as f:
        f.write(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"TARGET LANGUAGE: {target_lang.upper()}\n")
        f.write("-" * 30 + "\n")
        f.write(f"ORIGINAL:\n{original}\n\n")
        f.write(f"TRANSLATED:\n{translated}\n")
    return filename

def clear_logs():
    if os.path.exists(LOG_DIR):
        confirm = input("Are you sure you want to DELETE ALL LOGS? (y/n): ").lower()
        if confirm == 'y':
            shutil.rmtree(LOG_DIR)
            print("Logs cleared.")
            time.sleep(1)
    else:
        print("No logs found.")
        time.sleep(1)

# --- VOICE & INTERFACE ---

def get_voice():
    clear_terminal()
    sys.__stdout__.write("--- PREPARING MICROPHONE ---\n")
    sys.__stdout__.flush()
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 100.0 
    with deep_muzzle():
        try:
            mic = sr.Microphone()
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                for i in range(3, 0, -1):
                    sys.__stdout__.write(f"\r   Recording in {i}...   ")
                    sys.__stdout__.flush()
                    sys.__stdout__.write('\a')
                    time.sleep(1)
                sys.__stdout__.write("\n >>> RECORDING NOW <<<\n")
                sys.__stdout__.flush()
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=20)
                return recognizer.recognize_google(audio)
        except Exception:
            return None

def main():
    sys.stdout.write("\x1b]2;Universal Translator Pro\x07")
    sys.stdout.flush()

    translator = Translator()
    target = 'es' 
    clear_terminal()
    
    while True:
        print("="*55)
        print(f" UNIVERSAL TRANSLATOR PRO | TARGET: {LANGUAGES[target].upper()}")
        print("="*55)
        print("[V] Voice   [T] Text   [L] List Codes   [S] Set Lang")
        print("[O] Open Logs   [C] Clear Logs   [Q] Quit")
        choice = input("Choice: ").lower().strip()

        if choice == 'q': break
        elif choice == 'c': clear_logs(); clear_terminal()
        elif choice == 'l': 
            clear_terminal()
            for c, n in LANGUAGES.items(): print(f"{c}: {n}")
            input("\nPress Enter..."); clear_terminal()
        elif choice == 'o':
            if os.path.exists(LOG_DIR): subprocess.Popen(['pcmanfm', LOG_DIR])
            else: print("(!) No logs found.")
        elif choice == 's':
            code = input("Enter 2-letter Code: ").strip().lower()
            if code in LANGUAGES: target = code
            else: print("(!) Invalid code.")
        
        elif choice in ['v', 't']:
            text = ""
            if choice == 'v': text = get_voice()
            elif choice == 't':
                print("\n[Q] Quick Text  [B] Bulky (Newsletter)")
                sub = input("Select: ").lower().strip()
                if sub == 'q': text = input("Enter Text: ")
                elif sub == 'b':
                    print("\n--- BULKY MODE --- Paste then type 'DONE' on a new line.")
                    lines = []
                    while True:
                        line = input()
                        if line.strip().upper() == 'DONE': break
                        lines.append(line)
                    text = " ".join(lines)

            if text:
                try:
                    clean_text = text.replace('\n', ' ').strip()
                    segments = clean_text.replace('!', '.').replace('?', '.').split('.')
                    translated_parts = []
                    
                    print(f"\n[Processing {len(segments)} segments...]")
                    for segment in segments:
                        if len(segment.strip()) > 1:
                            try:
                                time.sleep(0.3)
                                res = translator.translate(segment.strip(), dest=target)
                                if res and res.text:
                                    translated_parts.append(res.text)
                                    sys.stdout.write("█")
                                    sys.stdout.flush()
                            except:
                                sys.stdout.write("░")
                                sys.stdout.flush()
                    
                    final_translation = ". ".join(translated_parts) + "."
                    
                    # Save to log (the reliable way to "copy" text)
                    save_log(text, final_translation, LANGUAGES[target])
                    
                    print(f"\n\nTRANSLATED:\n{final_translation}\n")
                    
                    tts = gTTS(text=final_translation, lang=target)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    pygame.mixer.music.load(fp)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy(): time.sleep(0.1)
                except Exception as e:
                    print(f"\n(!) System Error: {e}")

if __name__ == "__main__":
    main()
