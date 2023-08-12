import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write    
import shutil
import logging
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment
import os
import soundfile as sf
import tempfile
MODEL = None


def load_model(version):
    print("Loading model", version)
    return MusicGen.get_pretrained(version)

def predict(model, text, melody, duration, topk, topp, temperature, cfg_coef):
    global MODEL
    topk = int(topk)
    if MODEL is None or MODEL.name != model:
        MODEL = load_model(model)

    if duration > MODEL.lm.cfg.dataset.segment_duration:
        # raise gr.Error("MusicGen currently supports durations of up to 30 seconds!")
        print("MusicGen currently supports durations of up to 30 seconds!")
        # return
    MODEL.set_generation_params(
        use_sampling=True,
        top_k=topk,
        top_p=topp,
        temperature=temperature,
        cfg_coef=cfg_coef,
        duration=duration,
    )

    if melody:
        sr, melody = melody[0], torch.from_numpy(melody[1]).to(MODEL.device).float().t().unsqueeze(0)
        # print(melody.shape)
        if melody.dim() == 2:
            melody = melody[None]
        melody = melody[..., :int(sr * MODEL.lm.cfg.dataset.segment_duration)]
        output = MODEL.generate_with_chroma(
            descriptions=[text],
            melody_wavs=melody,
            melody_sample_rate=sr,
            progress=False
        )
    else:
        output = MODEL.generate(descriptions=[text], progress=False)

    output = output.detach().cpu().numpy()
    return MODEL.sample_rate, output

def predict_and_save(model, text, melody, duration, topk, topp, temperature, cfg_coef, filename):
    global MODEL
    topk = int(topk)
    if MODEL is None or MODEL.name != model:
        MODEL = load_model(model)

    if duration > MODEL.lm.cfg.dataset.segment_duration:
        # raise gr.Error("MusicGen currently supports durations of up to 30 seconds!")
        print("MusicGen currently supports durations of up to 30 seconds!")
        # return
    MODEL.set_generation_params(
        use_sampling=True,
        top_k=topk,
        top_p=topp,
        temperature=temperature,
        cfg_coef=cfg_coef,
        duration=duration,
    )

    
    if melody:
        sr, melody = melody[0], torch.from_numpy(melody[1]).to(MODEL.device).float().t().unsqueeze(0)
        # print(melody.shape)
        if melody.dim() == 2:
            melody = melody[None]
        melody = melody[..., :int(sr * MODEL.lm.cfg.dataset.segment_duration)]
        output = MODEL.generate_with_chroma(
            descriptions=[text],
            melody_wavs=melody,
            melody_sample_rate=sr,
            progress=False
        )
    else:
        output = MODEL.generate(descriptions=[text], progress=True)

    output = output.detach().cpu()
    output = output.squeeze()

    # Save the audio file
    audio_write(filename, output, MODEL.sample_rate, strategy="loudness", loudness_compressor=True)

    return MODEL.sample_rate, output

def save_audio(model, text, melody, duration, topk, topp, temperature, cfg_coef, filename):
    sample_rate, output = predict(model, text, melody, duration, topk, topp, temperature, cfg_coef)

    # Check the dimensions of the output and reduce if necessary
    if output.ndim > 2:
        output = output.squeeze()

    # Save the audio file
    audio_write(filename, torch.from_numpy(output), sample_rate, strategy="loudness", loudness_compressor=True)

def add_audio_to_video(model, text, melody, duration, topk, topp, temperature, cfg_coef, video_filepath, keep_audio=False, audio_format="mp3"):
    dir_path = os.path.dirname(video_filepath)
    logging.basicConfig(filename=os.path.join(dir_path, 'log.log'), level=logging.INFO)
    logging.info(f'Called add_audio_to_video with log: {locals()}')

    if duration > 30:
        duration = 30
        print("MusicGen currently supports durations of up to 30 seconds, only the first 30 seconds will be used")
        
    sample_rate, output = predict(model, text, melody, duration, topk, topp, temperature, cfg_coef)

    if output.ndim > 2:
        output = output.squeeze()

    temp_audio_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    temp_audio_filepath = temp_audio_file.name

    sf.write(temp_audio_file.name, output, sample_rate)

    audio = AudioFileClip(temp_audio_file.name)

    video = VideoFileClip(video_filepath)

    video_with_audio = video.set_audio(audio)

    output_video_filepath = os.path.splitext(video_filepath)[0] + "_with_audio.mp4"

    video_with_audio.write_videofile(output_video_filepath)

    audio.close()
    video.close()
    video_with_audio.close()
    temp_audio_file.close()

    if keep_audio:
        if audio_format == "wav":
            output_audio_filepath = os.path.splitext(video_filepath)[0] + "_audio.wav"
            shutil.move(temp_audio_filepath, output_audio_filepath)
        elif audio_format == "mp3":
            output_audio_filepath = os.path.splitext(video_filepath)[0] + "_audio.mp3"
            audio = AudioSegment.from_wav(temp_audio_filepath)
            audio.export(output_audio_filepath, format="mp3")
            os.unlink(temp_audio_filepath)  # delete the temporary .wav file
        else:
            raise ValueError("Unsupported audio_format. Please choose either 'wav' or 'mp3'.")
            
    return output_video_filepath
