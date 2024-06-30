import whisper

model = whisper.load_model("base")
result = model.transcribe("/Users/lism/Program/WebStormProjects/slidev-praise/public/assets/media/001_.mp3")
print(result["text"])