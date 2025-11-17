"""
36. Text to Speech - 텍스트 음성 변환
"""
import pyttsx3
from gtts import gTTS
import os

class TextToSpeech:
    """pyttsx3를 이용한 오프라인 TTS"""

    def __init__(self, rate=150, volume=1.0):
        """
        Args:
            rate: 말하기 속도 (기본 150)
            volume: 음량 (0.0 ~ 1.0)
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

    def speak(self, text):
        """텍스트를 음성으로 출력"""
        self.engine.say(text)
        self.engine.runAndWait()

    def save_to_file(self, text, filename='output.mp3'):
        """텍스트를 음성 파일로 저장"""
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        print(f"Audio saved to {filename}")

    def get_voices(self):
        """사용 가능한 음성 목록"""
        voices = self.engine.getProperty('voices')
        return [(i, v.name) for i, v in enumerate(voices)]

    def set_voice(self, voice_id):
        """음성 설정"""
        voices = self.engine.getProperty('voices')
        if 0 <= voice_id < len(voices):
            self.engine.setProperty('voice', voices[voice_id].id)

    def set_rate(self, rate):
        """말하기 속도 설정"""
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """음량 설정 (0.0 ~ 1.0)"""
        self.engine.setProperty('volume', volume)

class GoogleTTS:
    """Google Text-to-Speech (온라인)"""

    @staticmethod
    def speak(text, lang='en', slow=False):
        """텍스트를 음성으로 출력"""
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save("temp_speech.mp3")

        # 플레이 (OS별로 다름)
        if os.name == 'nt':  # Windows
            os.system("start temp_speech.mp3")
        elif os.name == 'posix':  # Mac/Linux
            os.system("afplay temp_speech.mp3" if os.uname().sysname == 'Darwin' else "mpg123 temp_speech.mp3")

    @staticmethod
    def save_to_file(text, filename='output.mp3', lang='en', slow=False):
        """텍스트를 음성 파일로 저장"""
        tts = gTTS(text=text, lang=lang, slow=slow)
        tts.save(filename)
        print(f"Audio saved to {filename}")

    @staticmethod
    def get_languages():
        """지원하는 언어 목록"""
        from gtts import lang
        return lang.tts_langs()

class Narrator:
    """텍스트 읽어주기"""

    def __init__(self, tts_engine='pyttsx3'):
        """
        Args:
            tts_engine: 'pyttsx3' 또는 'gtts'
        """
        self.tts_engine = tts_engine

        if tts_engine == 'pyttsx3':
            self.tts = TextToSpeech()
        else:
            self.tts = GoogleTTS()

    def read_text(self, text):
        """텍스트 읽기"""
        if self.tts_engine == 'pyttsx3':
            self.tts.speak(text)
        else:
            self.tts.speak(text)

    def read_file(self, filename):
        """파일 내용 읽기"""
        with open(filename, 'r', encoding='utf-8') as f:
            text = f.read()

        # 긴 텍스트를 청크로 나누기
        chunks = self._split_text(text, max_length=500)

        for i, chunk in enumerate(chunks, 1):
            print(f"Reading chunk {i}/{len(chunks)}...")
            self.read_text(chunk)

    def _split_text(self, text, max_length=500):
        """텍스트를 청크로 분할"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            if current_length + len(word) > max_length:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

# 사용 예제
if __name__ == '__main__':
    print("=== Text to Speech Demo ===\n")

    # pyttsx3 사용
    print("1. Using pyttsx3 (offline)")
    try:
        tts = TextToSpeech(rate=150)

        # 음성 목록
        voices = tts.get_voices()
        print(f"Available voices: {len(voices)}")
        for idx, name in voices[:3]:  # 처음 3개만 표시
            print(f"  {idx}: {name}")

        # 말하기
        text = "Hello! This is a text to speech demonstration."
        print(f"\nSpeaking: {text}")
        tts.speak(text)

        # 파일로 저장
        tts.save_to_file(text, "speech_output.mp3")

    except Exception as e:
        print(f"pyttsx3 error: {e}")
        print("Install with: pip install pyttsx3")

    # Google TTS 사용
    print("\n2. Using Google TTS (online)")
    try:
        # 지원 언어
        languages = GoogleTTS.get_languages()
        print(f"Supported languages: {len(languages)}")
        print(f"Examples: {list(languages.items())[:5]}")

        # 영어
        text_en = "This is Google Text to Speech."
        GoogleTTS.save_to_file(text_en, "gtts_english.mp3", lang='en')

        # 한국어
        text_ko = "안녕하세요. 구글 텍스트 음성 변환입니다."
        GoogleTTS.save_to_file(text_ko, "gtts_korean.mp3", lang='ko')

        # 일본어
        text_ja = "こんにちは。グーグルテキスト音声変換です。"
        GoogleTTS.save_to_file(text_ja, "gtts_japanese.mp3", lang='ja')

    except Exception as e:
        print(f"gtts error: {e}")
        print("Install with: pip install gtts")

    # Narrator 사용
    print("\n3. Using Narrator")
    narrator = Narrator('pyttsx3')

    # 짧은 텍스트
    story = """
    Once upon a time, there was a programmer who loved Python.
    They created amazing applications and shared them with the world.
    """

    print("Reading story...")
    narrator.read_text(story.strip())

    print("\nDemo complete!")
