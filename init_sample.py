from TTS.api import TTS

tts = TTS("tts_models/en/vctk/vits")
for i, speaker in enumerate(tts.speakers):
    tts.tts_to_file(
        text="The quick brown fox jumps over the lazy dog",
        speaker=speaker,
        file_path=f"static/samples/{i}.wav")
