import tensorflow as tf
import cv2
from PIL import Image
from collections import Counter


class_labels = {
    "alcohol": 0,
    "bloody_scenes": 1,
    "drugs": 2,
    "porn": 3,
    "smoking": 4,
    "safe_content": 5,
}
img_height, img_width = 224, 224

model = tf.keras.models.load_model("./models/model_1716044946.keras")
# audio_model = vosk.Model("./audio_model/vosk-model-small-ru-0.22")
# rec = vosk.KaldiRecognizer(audio_model, 16000)


def classify_image(image: Image) -> tuple[str, float]:
    img = image.resize((img_height, img_width))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) / 255.0

    predictions = model.predict(img_array)
    predicted_class = tf.argmax(predictions[0]).numpy()
    return list(class_labels.keys())[predicted_class], max(predictions[0])


def classify_video(capture: cv2.VideoCapture):
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    step = frame_count // 30

    results = {}

    cur_frame = 0
    while cur_frame < frame_count:
        ret, frame = capture.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)

        class_label, confidence = classify_image(img)

        if class_label not in results:
            results[class_label] = []
        results[class_label].append(round(confidence * 100))

        print(f"Frame {cur_frame}: {class_label} ({confidence:.2f})")

        capture.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
        cur_frame += step

    capture.release()

    risk_categories = {}
    for category, values in results.items():
        risk_categories[category] = (len(values), sum(values))

    return risk_categories


# def classify_audio(url: str):
#     response = requests.get(url)

#     with open('audio.wav', 'wb') as f:
#         f.write(response.content)

#     # for chunk in response.iter_content(chunk_size=256000):
#     #     if chunk:
#     #         rec.AcceptWaveform(chunk)
#     #         s = rec.PartialResult()
#     #         print(s)

#     # return rec.FinalResult()
