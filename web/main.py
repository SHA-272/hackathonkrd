from flask import Flask, request, jsonify, render_template
import time
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

    start_time = time.time()

    capture = videostream_extractor.get_video_stream(url)

    print('Video extract', time.time() - start_time)
    extract_time = time.time()

    if not capture.isOpened():
        return jsonify({"error": "The video stream cannot be opened"}), 400

    result = classificator.classify_video(capture)

    print("Classificate", time.time() - extract_time)

    results = {"result": result}
    return jsonify(results)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
