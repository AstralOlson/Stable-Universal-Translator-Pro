import os
import sys
import io
import time
import contextlib
import subprocess
import shutil
import re
from datetime import datetime

# --- Silence the startup noise and all false errors and nonexistant driver failures ---
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

# Initializing libraries
with deep_muzzle():
    import pygame
    import speech_recognition as sr
    from googletrans import Translator, LANGUAGES
    from gtts import gTTS
    pygame.mixer.init()

# --- HARDENED LOGGING / SECURITY ---
# Force absolute path resolution to prevent path traversal
BASE_LOG_DIR = os.path.abspath(os.path.expanduser("~/Desktop/Translator_Logs"))

def safe_save_log(original, translated, target_lang):
    """Saves session with path traversal protection."""
    if not os.path.exists(BASE_LOG_DIR):
        os.makedirs(BASE_LOG_DIR, mode=0o755)
    
    # Strip everything except letters to prevent a filename injection
    clean_lang = re.sub(r'[^a-zA-Z]', '', target_lang)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Trans_{clean_lang}_{timestamp}.txt"
    
    # Calculate absolute path and verify boundary
    target_path = os.path.abspath(os.path.join(BASE_LOG_DIR, filename))
    if not target_path.startswith(BASE_LOG_DIR):
        print("(!) Security Block: Invalid path detected.")
        return None

    with open(target_path, "w") as f:
        f.write(f"DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"ORIGINAL:\n{original}\n\n")
        f.write(f"TRANSLATED:\n{translated}\n")
    return filename

def safe_clear_logs():
    """Safely purges logs within the boundary."""
    if os.path.exists(BASE_LOG_DIR):
        confirm = input("Are you sure you want to DELETE ALL LOGS? (y/n): ").lower()
        if confirm == 'y':
            for filename in os.listdir(BASE_LOG_DIR):
                file_path = os.path.join(BASE_LOG_DIR, filename)
                # Strict check: only delete if inside our log folder 
                if os.path.abspath(file_path).startswith(BASE_LOG_DIR):
                    try:
                        if os.path.isfile(file_path): os.unlink(file_path)
                        elif os.path.isdir(file_path): shutil.rmtree(file_path)
                    except Exception as e: print(f"Error: {e}")
            print("Logs cleared safely.")
            time.sleep(1)
    else:
        print("No logs found.")
        time.sleep(1)

# --- CORE TRANSLATION & UI the good stuff ---

def get_voice():
    clear_terminal()
    sys.__stdout__.write("--- PREPARING MICROPHONE ---\n")
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 2.0 
    with deep_muzzle():
        try:
            mic = sr.Microphone()
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                for i in range(3, 0, -1):
                    sys.__stdout__.write(f"\r   Recording in {i}...   ")
                    sys.__stdout__.flush()
                    time.sleep(1)
                sys.__stdout__.write("\n >>> RECORDING NOW <<<\n")
                sys.__stdout__.flush()
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=20)
                return recognizer.recognize_google(audio)
        except Exception:
            return None

def main():
    sys.stdout.write("\x1b]2;Universal Translator Pro\x07")
    translator = Translator()
    target = 'es' 
    clear_terminal()

    #-----------  MAIN MENU ------------
    
    while True:
        print("="*55)
        print(f" UNIVERSAL TRANSLATOR PRO | TARGET: {LANGUAGES[target].upper()}")
        print("="*55)
        print("[V] Voice   [T] Text   [L] List Codes   [S] Set Language")
        print("[O] Open Logs   [C] Clear Logs   [Q] Quit")
        choice = input("Choice: ").lower().strip()

        if choice == 'q': break
        elif choice == 'c': safe_clear_logs(); clear_terminal()
        elif choice == 'l': 
            clear_terminal(); [print(f"{c}: {n}") for c, n in LANGUAGES.items()]
            input("\nPress Enter..."); clear_terminal()
        elif choice == 'o':
            if os.path.exists(BASE_LOG_DIR): subprocess.Popen(['pcmanfm', BASE_LOG_DIR])
        elif choice == 's':
            code = input("Enter 2-letter Code: ").strip().lower()
            if code in LANGUAGES: target = code
        
        elif choice in ['v', 't']:
            text = ""
            if choice == 'v': text = get_voice()
            elif choice == 't':
                print("\n[Q] Quick Text  [B] Bulky (Newsletter)")
                sub = input("Select: ").lower().strip()
                if sub == 'q': text = input("Enter Text: ")
                elif sub == 'b':
                    print("\n--- BULKY MODE --- Paste then type 'DONE'.")
                    lines = []
                    while True:
                        line = input()
                        if line.strip().upper() == 'DONE': break
                        lines.append(line)
                    text = " ".join(lines)

            if text:
                try:
                    segments = text.replace('!', '.').replace('?', '.').split('.')
                    translated_parts = []
                    print(f"\n[Processing {len(segments)} segments...]")
                    for segment in segments:
                        if len(segment.strip()) > 1:
                            time.sleep(0.3)
                            res = translator.translate(segment.strip(), dest=target)
                            if res: translated_parts.append(res.text)
                            sys.stdout.write("█"); sys.stdout.flush()
                    
                    final_translation = ". ".join(translated_parts) + "."
                    safe_save_log(text, final_translation, LANGUAGES[target])
                    
                    print(f"\n\nTRANSLATED:\n{final_translation}\n")
                    
                    tts = gTTS(text=final_translation, lang=target)
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    pygame.mixer.music.load(fp)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy(): time.sleep(0.1)
                except Exception as e: print(f"\n(!) Error: {e}")

if __name__ == "__main__":
    main()
