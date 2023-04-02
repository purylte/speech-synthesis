from celery import Celery
import os
import requests
import shutil
from TTS.api import TTS

from utils import get_new_dir

celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task()
def start_task(prompt, speaker_index, output_file_name):
    directory = get_new_dir()
    try:
        output_path = generate_tts(
            prompt, speaker_index, directory, output_file_name)
        url = upload_video(output_path, output_file_name)
    finally:
        cleanup(directory)
    return url

# celery -A worker worker -l INFO --pool=solo


def generate_tts(prompt, speaker_index, directory, output_file_name):
    output_path = f"{directory}/{output_file_name}.wav"
    tts = TTS("tts_models/en/vctk/vits")
    if (speaker_index >= len(tts.speakers) or speaker_index < 0):
        raise ValueError(
            f"Speaker index out of range, please choose a speaker index between 0 and {len(tts.speakers)-1}")

    tts.tts_to_file(
        text=prompt,
        speaker=tts.speakers[speaker_index],
        file_path=output_path)
    return output_path


def upload_video(file_path, url_name):
    with open(file_path, 'rb') as f:
        data = f.read()
    response = requests.put(f'https://bashupload.com/{url_name}', data=data)
    text_response = response.text
    start_index = text_response.find('https://bashupload.com/')
    end_index = text_response.find('\n', start_index)
    url = text_response[start_index:end_index]
    return url


def cleanup(directory):
    shutil.rmtree(directory)
