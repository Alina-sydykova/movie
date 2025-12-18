# subtitle_final.py
import whisper
import pysrt
import os
import sys
from datetime import timedelta
import torch
from transformers import pipeline

# === КРИТИЧЕСКИ ВАЖНАЯ СТРОКА: Указываем системе, где искать ffmpeg/ffprobe ===
# Если вы положили ffmpeg в другую папку, измените путь ниже!
os.environ["PATH"] = r"C:\ffmpeg\bin" + os.pathsep + os.environ["PATH"]

class SubtitleGenerator:
    def __init__(self, model_size="base"):
        print(f"Загружаю модель Whisper {model_size}...")
        self.model = whisper.load_model(model_size)
    # Initialize translation pipeline
    # For Kyrgyz translation, use "Helsinki-NLP/opus-mt-en-ky" (English to Kyrgyz)
    # For a general model that supports Kyrgyz, use "facebook/mbart-large-50-many-to-many-mmt"
        self.translator = pipeline("translation",
                                model="facebook/mbart-large-50-many-to-many-mmt",
                                device=0 if torch.cuda.is_available() else -1)
    
    def format_time(self, seconds):
        """Форматирование времени для SRT"""
        td = timedelta(seconds=seconds)
        hours = td.seconds // 3600
        minutes = (td.seconds % 3600) // 60
        seconds = td.seconds % 60
        milliseconds = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    def transcribe(self, video_path, language=None):
        """Транскрибируем видео напрямую через Whisper"""
        print(f"Начинаю транскрибацию видео...")
        result = self.model.transcribe(
            video_path,
            language=language,
            verbose=False,
            word_timestamps=True
        )
        return result
    
    def create_srt(self, segments, output_path):
        """Создаем файл субтитров .srt"""
        print(f"Создаю файл субтитров...")
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, segment in enumerate(segments, 1):
                start = self.format_time(segment['start'])
                end = self.format_time(segment['end'])
                text = segment['text'].strip()
                f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
        return output_path
    
    def translate_srt(self, srt_path, src_lang='en', dest_lang='ky'):
        print(f"Перевожу субтитры с {src_lang} на {dest_lang}...")
        subs = pysrt.open(srt_path)
    
        for i, sub in enumerate(subs, 1):
                try:
            # For mBART, set language codes for the tokenizer
            # Note: Language codes for mBART are like 'en_XX', 'ky_XX'. You may need to check the specific code for Kyrgyz.
            # Example for translating from English to French:
            # self.translator.tokenizer.src_lang = "en_XX"
            # result = self.translator(sub.text, forced_bos_token_id=self.translator.tokenizer.lang_code_to_id["fr_XX"])
            
            # For a Helsinki-NLP model (e.g., opus-mt-en-ky), the call is simpler:
                    result = self.translator(sub.text, src_lang=src_lang, tgt_lang=dest_lang)[0]
                    translated_text = result['translation_text']
            
            # Use SubRipItem for pysrt
                    new_sub = pysrt.SubRipItem(index=sub.index, start=sub.start, end=sub.end, text=translated_text)
                    subs[i-1] = new_sub  # Replace the subtitle in the list
            
                    if i % 20 == 0:
                        print(f"  Переведено {i}/{len(subs)} строк...")
                except Exception as e:
                    print(f"  Ошибка в строке {i}: {e}. Использую оригинальный текст.")
            # Keep original subtitle on error
    
        output_path = srt_path.replace('.srt', f'_{dest_lang}.srt')
        subs.save(output_path, encoding='utf-8')
        return output_path

def main():
    if len(sys.argv) < 2:
        print("Использование: python subtitle_final.py <видео_файл> [язык]")
        print("Пример: python subtitle_final.py video.mp4 ru")
        return
    
    video_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(video_file):
        print(f"Ошибка: Файл '{video_file}' не найден.")
        return
    
    # Инициализация
    generator = SubtitleGenerator(model_size="base")  # Можно заменить на "small" для качества
    
    try:
        # 1. Транскрибация
        result = generator.transcribe(video_file, language)
        print("Транскрибация завершена.")
        
        # 2. Создание оригинальных субтитров
        base_name = os.path.splitext(video_file)[0]
        original_srt = f"{base_name}.srt"
        generator.create_srt(result['segments'], original_srt)
        print(f"Создан файл: {original_srt}")
        
        # 3. Перевод
        translated_srt = generator.translate_srt(original_srt)
        print(f"Создан файл: {translated_srt}")
        
        print("\n" + "="*50)
        print("✅ Готово! Все файлы созданы:")
        print(f"   📄 Оригинал (исходный язык): {original_srt}")
        print(f"   📄 Перевод (кыргызский): {translated_srt}")
        print("="*50)
        
    except FileNotFoundError as e:
        print(f"\n❌ Критическая ошибка: Не найден ffmpeg или ffprobe.")
        print(f"   Убедитесь, что путь в скрипте (строка 12) ведет к папке 'bin' с ffmpeg.exe")
        print(f"   Текущий путь в скрипте: {os.environ['PATH'].split(os.pathsep)[0]}")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")



if __name__ == "__main__":
    main()