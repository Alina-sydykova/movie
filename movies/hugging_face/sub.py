import whisper
import pysrt
import os
import sys
import time
import json
from datetime import timedelta
import requests  # Убедитесь, что установлена: pip install requests

os.environ["PATH"] = r"C:\ffmpeg\bin" + os.pathsep + os.environ["PATH"]

class SubtitleGenerator:
    def __init__(self, model_size="base"):
        print(f"Загружаю модель Whisper {model_size}...")
        self.model = whisper.load_model(model_size)
        
        # 1. ИСПРАВЛЕННЫЙ АДРЕС API И КЛЮЧ (ваш ключ уже верный)
        self.api_url = "https://openl-translate.p.rapidapi.com/translate"
        self.api_key = "21d339758emsh9a614fe90158b2cp136f6djsnbc8fdc6a54d3"
        self.api_host = "openl-translate.p.rapidapi.com"
    
    # ... (МЕТОДЫ format_time, transcribe, create_srt ОСТАЮТСЯ БЕЗ ИЗМЕНЕНИЙ, как в вашем первоначальном коде) ...
    
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

    def translate_text_openl(self, text, target_lang='ky'):

        headers = {
        'x-rapidapi-key': self.api_key,
        'x-rapidapi-host': self.api_host,
        'Content-Type': "application/json"
        }
    
        payload = {
        "target_lang": target_lang,
        "text": text[:4000]
        }
    
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=15)
        
            if response.status_code == 200:
                result = response.json()
            # ИСПРАВЛЕНИЕ: используем правильный ключ из ответа API
                if 'translatedText' in result:
                    return result['translatedText']
                else:
                # Если структура всё ещё неожиданная, выводим её для отладки
                    print(f"  Неожиданная структура ответа API. Полный ответ: {result}")
                    return text
            else:
                print(f"  Ошибка API [{response.status_code}]: {response.text[:100]}")
                return text
            
        except requests.exceptions.RequestException as e:
            print(f"  Сетевая ошибка при обращении к API: {e}")
            return text
        except json.JSONDecodeError as e:
            print(f"  Ошибка разбора JSON от API: {e}")
            return text
    
    def translate_srt(self, srt_path, dest_lang='ky'):
        """Переводим файл .srt на кыргызский"""
        print(f"Перевожу субтитры на кыргызский через OpenL API...")
        subs = pysrt.open(srt_path)
        translated_subs = []
        
        total_lines = len(subs)
        for i, sub in enumerate(subs, 1):
            # Переводим текст строки субтитров
            translated_text = self.translate_text_openl(sub.text, dest_lang)
            
            # Создаем новый субтитр с переведенным текстом
            new_sub = pysrt.SubRipItem(
                index=sub.index,
                start=sub.start,
                end=sub.end,
                text=translated_text
            )
            translated_subs.append(new_sub)
            
            # Выводим прогресс каждые 5 строк и делаем паузу, чтобы не превысить лимиты API
            if i % 5 == 0 or i == total_lines:
                print(f"  Переведено {i}/{total_lines} строк...")
                time.sleep(0.3)  # Пауза, чтобы избежать ошибки 429 (Too Many Requests)
        
        # Сохраняем переведенные субтитры в новый файл
        output_path = srt_path.replace('.srt', '_ky.srt')
        pysrt.SubRipFile(items=translated_subs).save(output_path, encoding='utf-8')
        return output_path
    def convert_srt_to_vtt(self, srt_path, vtt_path=None):
        """Конвертирует SRT в формат WebVTT для корректной работы в браузере"""
        if vtt_path is None:
            vtt_path = srt_path.replace('.srt', '.vtt')
    
        try:
            with open(srt_path, 'r', encoding='utf-8') as srt_file:
                content = srt_file.read()
        
        # Добавляем заголовок WebVTT и конвертируем формат времени
            vtt_content = "WEBVTT\n\n" + content.replace(',', '.')
        
            with open(vtt_path, 'w', encoding='utf-8') as vtt_file:
                vtt_file.write(vtt_content)
        
            print(f"✅ Конвертирован в WebVTT: {vtt_path}")
            return vtt_path
        except Exception as e:
            print(f"❌ Ошибка конвертации: {e}")
            return None

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
    
    generator = SubtitleGenerator(model_size="base")
    
    try:
        # 1. Транскрибация
        result = generator.transcribe(video_file, language)
        print("Транскрибация завершена.")
        
        # 2. Создание оригинальных (английских) субтитров
        base_name = os.path.splitext(video_file)[0]
        original_srt = f"{base_name}.srt"
        generator.create_srt(result['segments'], original_srt)
        print(f"Создан файл: {original_srt}")
        
        # 3. Сразу создаем VTT-версию английских субтитров для сайта
        original_vtt = generator.convert_srt_to_vtt(original_srt)
        if original_vtt:
            print(f"Создана WebVTT версия (англ.): {original_vtt}")
        
        # 4. Перевод на кыргызский
        translated_srt = generator.translate_srt(original_srt)
        print(f"Создан файл: {translated_srt}")
        
        # 5. Создаем VTT-версию кыргызских субтитров для сайта
        translated_vtt = generator.convert_srt_to_vtt(translated_srt)
        if translated_vtt:
            print(f"Создана WebVTT версия (кырг.): {translated_vtt}")
        
        print("\n" + "="*50)
        print("✅ Готово! Все файлы созданы:")
        print(f"   📄 Оригинал (SRT, исходный язык): {original_srt}")
        print(f"   🌐 Оригинал (VTT, для сайта): {original_vtt}")
        print(f"   📄 Перевод (SRT, кыргызский): {translated_srt}")
        print(f"   🌐 Перевод (VTT, для сайта): {translated_vtt}")
        print("="*50)
        
    except FileNotFoundError as e:
        print(f"\n❌ Критическая ошибка: Не найден ffmpeg или ffprobe.")
        print(f"   Убедитесь, что путь в скрипте (строка 12) ведет к папке 'bin' с ffmpeg.exe")
        print(f"   Текущий путь в скрипте: {os.environ['PATH'].split(os.pathsep)[0]}")
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()