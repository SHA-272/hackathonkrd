import classificator, videostream_extractor

url = "https://www.youtube.com/watch?v=g6IJyPUwwPM"

audio_url = videostream_extractor.get_audio_stream(url)

text = classificator.classify_audio(audio_url)

print(text)
