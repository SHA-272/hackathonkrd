from flask import Flask, request, jsonify, render_template
import cv2
import classificator
import videostream_extractor

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/classify", methods=["POST"])
def classify():
    if "url" not in request.json:
        return jsonify({"error": "No url provided"}), 400

    url = request.json["url"]

    capture = cv2.VideoCapture(videostream_extractor.get_video_stream(url))

    if not capture:
        return jsonify({"error": "The video stream cannot be opened"}), 400

    if not capture.isOpened():
        return jsonify({"error": "The video stream cannot be opened"}), 400

    result = classificator.classify_video(capture)

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
