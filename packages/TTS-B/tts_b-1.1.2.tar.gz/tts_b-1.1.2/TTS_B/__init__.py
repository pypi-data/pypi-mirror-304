import os
import requests
import playsound
from typing import Union
from mutagen.mp3 import MP3  # Used to get the duration of MP3 files
import time

def generate_audio(message: str, voice: str = "Brian") -> Union[bytes, None]:
    url: str = f"https://api.streamelements.com/kappa/v2/speech?voice={voice}&text={{{message}}}"
    
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)AppleWebKit/537.36 (KHTML, like Gecoko)Chrome/119.0.0.0 Safari/537.36'}

    try:
        result = requests.get(url=url, headers=headers)
        return result.content
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def speak(message: str, voice: str = "Brian", folder: str = "", extension: str = ".mp3") -> None:
    try:
        result_content = generate_audio(message, voice)
        file_path = os.path.join(folder, f"{voice}{extension}")
        if os.path.exists(file_path):
            print("Audio file already exists.")
        else:
            os.open(file_path, "x")
            return
        
        if result_content:
            os.remove(file_path)
            # Save the audio file
            with open(file_path, "wb") as f:
                f.write(result_content)
            # Calculate the duration of the audio
            audio = MP3(file_path)
            # Play the audio
            playsound.playsound(file_path)     
        else:
            print("No audio content generated.")
    
    except Exception as e:
        print(f"Error during speak: {e}")