import os
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from .transcribe import Transcribe, TranscriptionOptions
from typing import Union, List
import time
import datetime

SampleRate = 44100  # Stream device recording frequency per second
BlockSize = 50  # Block size in milliseconds
Threshold = 0.2  # Minimum volume threshold to activate listening
Vocals = [50, 1000]  # Frequency range to detect sounds that could be speech
EndBlocks = 40  # Number of blocks to wait before sending to Whisper
ForceSendBlocks = 250 # Send the segment after 15 seconds

class Live:
    def __init__(
        self,
        model_path: str,
        task: str,
        language: str,
        threads: int,
        device: str,
        device_index: Union[int, List[int]],
        compute_type: str,
        verbose: bool,
        options: TranscriptionOptions,
    ):
        self.model_path = model_path
        self.task = task
        self.language = language
        self.threads = threads
        self.device = device
        self.device_index = device_index
        self.compute_type = compute_type
        self.verbose = verbose
        self.options = options

        self.running = True
        self.waiting = 0
        self.prevblock = self.buffer = np.zeros((0, 1))
        self.fileready = False
        self.speaking = False

    # A few alternative methods exist for detecting speech.. #indata.max() > Threshold
    # zero_crossing_rate = np.sum(np.abs(np.diff(np.sign(indata)))) / (2 * indata.shape[0]) # threshold 20

    def _is_there_voice(self, indata, frames):
        freq = np.argmax(np.abs(np.fft.rfft(indata[:, 0]))) * SampleRate / frames
        volume = np.sqrt(np.mean(indata**2))

        return volume > Threshold and Vocals[0] <= freq <= Vocals[1]

    def callback(self, indata, frames, _time, status):
        # if status: print(status) # for debugging, prints stream errors.
        if not any(indata):
            print(
                "\033[31m.\033[0m", end="", flush=True
            )  # if no input, prints red dots
            return

        voice = self._is_there_voice(indata, frames)

        # Silence and no nobody has started speaking
        if voice == False and self.speaking == False:
            return

        if voice:  # User speaking
            print(".", end="", flush=True)
#            if self.waiting < 1:
#                self.buffer = self.prevblock.copy()
            self.buffer = np.concatenate((self.buffer, indata))
            self.waiting = datetime.datetime.now()
            
            if not self.speaking:
                self.forcesend = datetime.datetime.now()
                
            self.speaking = True
            
        else:  # Silence after user has spoken
#            print(f"{self.waiting} - {self.forcesend}")

            forced = (datetime.datetime.now() - self.forcesend).seconds > 15

            if self.waiting < 0 or forced:
                # if enough silence has passed, write to file.
                self.fileready = True
                write("dictate.wav", SampleRate, self.buffer)
                self.buffer = np.zeros((0, 1))
                self.speaking = False
            else:
                self.buffer = np.concatenate((self.buffer, indata))

    def process(self):
        if self.fileready:
            print("\n\033[90mTranscribing..\033[0m")
            result = Transcribe().inference(
                "dictate.wav",
                model_path=self.model_path,
                task=self.task,
                language=self.language,
                threads=self.threads,
                device=self.device,
                device_index=self.device_index,
                compute_type=self.compute_type,
                verbose=self.verbose,
                options=self.options,
            )
            print(f"\033[1A\033[2K\033[0G{result['text']}")
            self.fileready = False

    #            self.prevblock = self.buffer = np.zeros((0, 1))

    def listen(self):
        print("\033[32mListening.. \033[37m(Ctrl+C to Quit)\033[0m")
        with sd.InputStream(
            channels=1,
            callback=self.callback,
            blocksize=int(SampleRate * BlockSize / 1000),
            samplerate=SampleRate,
        ):
            while self.running:
                self.process()

    def inference(self):
        try:
            self.listen()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            print("\n\033[93mQuitting..\033[0m")
            if os.path.exists("dictate.wav"):
                os.remove("dictate.wav")
