# test_simple.py
from transformers import pipeline

print("Тестируем простую модель перевода...")
try:
    # Более легкая модель
    translator = pipeline("translation", 
                         model="Helsinki-NLP/opus-mt-en-ky")
    
    result = translator("Hello, how are you?")
    print(f"✅ Перевод работает: {result[0]['translation_text']}")
    
    result = translator("This is a test of the translation system.")
    print(f"✅ Длинный текст: {result[0]['translation_text']}")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\nПопробуйте установить: pip install protobuf sentencepiece")