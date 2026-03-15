# Stable-Universal-Translator-Pro
A Miniature Translator that you can hold in the palm of your hand. It can translate up to 60 languages has voice to voice and text to speech options, and all runs on a Raspberry Pi 3.  It requires: pygame, SpeechRecognition, googletrans==3.1.0a0, and gTTS. 

Universal Translator Pro (Raspberry Pi 3 Edition)
A robust, voice-and-text translation suite engineered for stability on the Raspberry Pi 3. This tool is designed to handle everything from quick spoken phrases to massive multi-paragraph newsletters without crashing or hitting API rate limits.

Key Features
Bulky Text Mode: Custom segmentation algorithm breaks long documents into bite-sized pieces for reliable translation.

Stability Shield: Integrated 0.3s rate-limiting and NoneType error handling to prevent API-related crashes.

Hardware Noise Suppression: Built-in "Deep Muzzle" logic to keep the terminal interface clean of ALSA/Jack driver errors.

Automated Log Management: Automatically archives every session to ~/Desktop/Translator_Logs for easy retrieval and record-keeping.

🛠️ Quick Start Setup
For a fresh Raspberry Pi 3 setup, run these commands:

1. Install System Dependencies

Bash

     sudo apt update
Bash

    sudo apt install python3-venv portaudio19-dev libasound2-dev flac -y

3. Create a Virtual Environment

  Bash
 
    python3 -m venv Translator_env
Bash  

    source Translator_env/bin/activate

3. Install Python Libraries

  Bash
  
    pip install pygame speechrecognition googletrans==3.1.0a0 gTTS

 Usage

  [V] Voice: Record and translate audio (optimized for up to 20-second segments).

[T] Text: Choose Quick for single lines or Bulky for long-form newsletters.

[O] Open Logs: Instant access to your translation history in the Pi file manager.

[C] Clear Logs: One-touch maintenance to keep your storage clean.

Portions of this codebase were generated with the assistance of Gemini (Google AI) and curated/refined by Alexander Olson.

I built this as a way to handle long-form newsletters from other countries and languages on a Raspberry Pi 3, I noticed that there wasn't much out there in the way of universal tranlator projects and decided to engineer one from scratch. 

Compared to other AI Slop this code has had a history of fixes!:

I fixed ALSA/Jack driver noise on RPi 3 using a custom suppression context.

I implemented manual segmentation to bypass Google Translate’s 5k character limit.

I also hardened pathing against traversal attacks for better local security.

Where most designs fail, this one succeeds. Yes it use's google translate but google translate only has a certain charater limit. Where this code segments larger chunks out of the translation for massive amounts of text processing without the fear of losing data in segments. A user can copy and paste large articles in different languages and translate it all into legable containers on a small screen a small package. As well as logs all translations. 

*Built with a mix of manual engineering and AI-collaboration to solve Raspberry Pi 3 audio driver hurdles.*

I built this because in many parts of the world, high-end laptops are expensive, but a Raspberry Pi is accessible.

How it helps: A teacher in a remote area can use this script as a classroom tool to translate educational newsletters or global news for students, using a device that costs less than $50. The "Bulky Mode" allows them to process entire articles rather than just single sentences.

I built it to also be a digital preservationists and archivist
Because this script automatically logs every translation with a timestamp and security-hardened file paths, it is a "set-and-forget" logging tool.

How it helps: Researchers documenting foreign language broadcasts or interviews can use the Voice Mode to get a rough translation and immediately have a saved text file for their records.

I am also privacy-conscious:
By implementing Path Traversal protection and Regex Sanitization, I’ve created a script that is safer to run on a home network than many "generic" GitHub scripts.

How it helps: It serves as a Learning Template for other junior developers. It teaches them how to use AI tools responsibly by adding a "Human-in-the-Loop" for security layers.

As well as having accessibility options:
The combination of Speech-to-Text (STT) and Text-to-Speech (TTS) makes this a bidirectional accessibility bridge.

How it helps: A user with visual impairments can speak into the microphone and hear the translation read back to them, while a user with hearing or speech impairments can use the "Bulky Text" mode to communicate complex ideas through the Pi's speakers.
