from Remi_voice.remi_voice import remi_voice
from Remi_ear.remi_ear import remi_ear


talk = remi_voice()
hear = remi_ear()
# def test_remi_voice():
#     talk.process_and_play("Hello, I am Remi. I am a voice assistant.", 'cheerful')
#     talk.process_and_play("How can I assist you today?", 'default')
#     talk.process_and_play("I can help with tasks like setting reminders, playing music, and answering questions.", 'sad')
#     talk.process_and_play("Feel free to ask me anything!", 'friendly')
def test_remi_tom():
    audio_file = 'test.wav'
    heared_text = hear.record_audio('test.wav')
    talk.process_and_play(heared_text, 'cheerful')


if __name__ == "__main__":
    test_remi_tom()