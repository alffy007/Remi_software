import os
import torch
from openvoice import se_extractor
from openvoice.api import BaseSpeakerTTS, ToneColorConverter
import pyaudio
import wave

ckpt_base = 'Remi_voice/checkpoints_v2/base_speakers\EN'
ckpt_converter = 'Remi_voice/checkpoints_v2/converter'
device="cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs'
print(f"Using device: {device}")
base_speaker_tts = BaseSpeakerTTS(f'{ckpt_base}/config.json', device=device)
base_speaker_tts.load_ckpt(f'{ckpt_base}/checkpoint.pth')

tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

os.makedirs(output_dir, exist_ok=True)

source_se = torch.load(f'{ckpt_base}/en_default_se.pth').to(device)


reference_speaker = 'Remi_voice/spongebib.mp3' # This is the voice you want to clone
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, target_dir='Remi_voice/processed', vad=True)


save_path = f'{output_dir}/output_en_default.wav'


# Function to play audio using PyAudio
def play_audio(file_path):
    # Open the audio file
    wf = wave.open(file_path, "rb")
    # Create a PyAudio instance
    p = pyaudio.PyAudio()
    # Open a stream to play audio
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
    )
    # Read and play audio data
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    # Stop and close the stream and PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()



class remi_voice:
    def process_and_play(self, text, tts_mod):
        src_path = f'{output_dir}/tmp.wav'
        base_speaker_tts.tts(text, src_path, speaker=tts_mod, language='English', speed=1.1)
            # Run the tone color converter
        encode_message = "@MyShell"
        tone_color_converter.convert(
                audio_src_path=src_path,
                src_se=source_se,
                tgt_se=target_se,
                output_path=save_path,
                message=encode_message
                )
        print("Audio generated successfully with openvoice.")
        play_audio(save_path) 
