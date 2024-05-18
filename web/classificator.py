import tensorflow as tf
import cv2
from PIL import Image
from collections import Counter
import speech_recognition

class_labels = {
    'alcohol': 0,
    'bloody_scenes': 1,
    'drugs': 2,
    'porn': 3,
    'smoking': 4,
    'safe_content': 5
}
img_height, img_width = 224, 224

model = tf.keras.models.load_model('../models/model_1716044946.keras')

def classify_image(image: Image) -> tuple[str, float]:
    img = image.resize((img_height, img_width))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) / 255.0  

    predictions = model.predict(img_array)
    predicted_class = tf.argmax(predictions[0]).numpy()
    return list(class_labels.keys())[predicted_class], max(predictions[0])

def classify_video(capture: cv2.VideoCapture) -> str:
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    results = []

    cur_frame = 0
    while cur_frame < frame_count:
        ret, frame = capture.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        
        class_label, confidence = classify_image(img)
        results.append((cur_frame, class_label, confidence))

        print(f"Frame {cur_frame}: {class_label} ({confidence:.2f})")

        capture.set(cv2.CAP_PROP_POS_FRAMES, cur_frame)
        cur_frame += fps * 60

    capture.release()

    label_counts = Counter([result[1] for result in results])
    
    most_common_label = label_counts.most_common(1)[0][0]
    return most_common_label

def classify_audio():
    speech_recognition.AudioData()