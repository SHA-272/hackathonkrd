import ffmpeg
import pyaudio
import wave
import speech_recognition as sr
import threading

# Параметры аудио
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

# Ссылка на видеопоток
video_url = "https://www.youtube.com/watch?v=OJfiesQBE_8&list=PLbRZPwhakfXuGpEsuWwwQoOtRKn1lPzX1"
output_video_file = "output_video.mp4"

# Функция для сохранения видеопотока
def save_video_stream(video_url, output_video_file):
    (
        ffmpeg
        .input(video_url)
        .output(output_video_file)
        .run()
    )

# Создаем поток для сохранения видеопотока
video_thread = threading.Thread(target=save_video_stream, args=(video_url, output_video_file))
video_thread.start()

# Создаем поток с помощью ffmpeg, который захватывает только аудио
process = (
    ffmpeg
    .input(video_url)
    .output('pipe:', format='wav', acodec='pcm_s16le', ac=1, ar=RATE)
    .run_async(pipe_stdout=True)
)

# Настройка pyaudio для записи
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Инициализация распознавателя речи
recognizer = sr.Recognizer()

print("Начало распознавания речи из видеопотока...")

try:
    while True:
        # Чтение данных из ffmpeg
        audio_data = process.stdout.read(CHUNK)
        if not audio_data:
            break

        # Создаем аудиофайл из байтового потока
        audio_segment = wave.open(audio_data, 'rb')

        # Конвертируем аудиофайл в аудиоданные для распознавания речи
        audio = sr.AudioData(audio_segment.readframes(audio_segment.getnframes()), RATE, audio_segment.getsampwidth())

        # Распознавание речи
        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("Распознанный текст: " + text)
        except sr.UnknownValueError:
            print("Речь не распознана")
        except sr.RequestError as e:
            print(f"Ошибка сервиса распознавания речи; {e}")

finally:
    # Закрытие потоков и завершение процесса
    stream.stop_stream()
    stream.close()
    p.terminate()
    process.stdout.close()
    process.wait()

    # Ждем завершения записи видеопотока
    video_thread.join()

print("Распознавание завершено и видеопоток сохранен")
