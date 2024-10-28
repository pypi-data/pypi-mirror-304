from typing import Iterable, List, Optional, Union
from urllib.parse import urlparse
import subprocess
import platform
import logging
import socket
import time
import sys
import os

DEFAULT_CONTROL_URL = "ws://127.0.0.1:8011"
DEFAULT_DATA_URL = "ws://127.0.0.1:8012"

INIT_MODEL_TRANSCRIPTION = "tiny"
INIT_MODEL_TRANSCRIPTION_REALTIME = "tiny"
INIT_REALTIME_PROCESSING_PAUSE = 0.2
INIT_SILERO_SENSITIVITY = 0.4
INIT_WEBRTC_SENSITIVITY = 3
INIT_POST_SPEECH_SILENCE_DURATION = 0.6
INIT_MIN_LENGTH_OF_RECORDING = 0.5
INIT_MIN_GAP_BETWEEN_RECORDINGS = 0
INIT_WAKE_WORDS_SENSITIVITY = 0.6
INIT_PRE_RECORDING_BUFFER_DURATION = 1.0
INIT_WAKE_WORD_ACTIVATION_DELAY = 0.0
INIT_WAKE_WORD_TIMEOUT = 5.0
INIT_WAKE_WORD_BUFFER_DURATION = 0.1
ALLOWED_LATENCY_LIMIT = 100

# TIME_SLEEP = 0.02
SAMPLE_RATE = 16000
BUFFER_SIZE = 512
# INT16_MAX_ABS_VALUE = 32768.0

INIT_HANDLE_BUFFER_OVERFLOW = False
if platform.system() != 'Darwin':
    INIT_HANDLE_BUFFER_OVERFLOW = True

class AudioToTextRecorderClient:
    """
    A class responsible for capturing audio from the microphone, detecting
    voice activity, and then transcribing the captured audio using the
    `faster_whisper` model.
    """

    def __init__(self,
                 model: str = INIT_MODEL_TRANSCRIPTION,
                 language: str = "",
                 compute_type: str = "default",
                 input_device_index: int = None,
                 gpu_device_index: Union[int, List[int]] = 0,
                 device: str = "cuda",
                 on_recording_start=None,
                 on_recording_stop=None,
                 on_transcription_start=None,
                 ensure_sentence_starting_uppercase=True,
                 ensure_sentence_ends_with_period=True,
                 use_microphone=True,
                 spinner=True,
                 level=logging.WARNING,

                 # Realtime transcription parameters
                 enable_realtime_transcription=False,
                 use_main_model_for_realtime=False,
                 realtime_model_type=INIT_MODEL_TRANSCRIPTION_REALTIME,
                 realtime_processing_pause=INIT_REALTIME_PROCESSING_PAUSE,
                 on_realtime_transcription_update=None,
                 on_realtime_transcription_stabilized=None,

                 # Voice activation parameters
                 silero_sensitivity: float = INIT_SILERO_SENSITIVITY,
                 silero_use_onnx: bool = False,
                 silero_deactivity_detection: bool = False,
                 webrtc_sensitivity: int = INIT_WEBRTC_SENSITIVITY,
                 post_speech_silence_duration: float = (
                     INIT_POST_SPEECH_SILENCE_DURATION
                 ),
                 min_length_of_recording: float = (
                     INIT_MIN_LENGTH_OF_RECORDING
                 ),
                 min_gap_between_recordings: float = (
                     INIT_MIN_GAP_BETWEEN_RECORDINGS
                 ),
                 pre_recording_buffer_duration: float = (
                     INIT_PRE_RECORDING_BUFFER_DURATION
                 ),
                 on_vad_detect_start=None,
                 on_vad_detect_stop=None,

                 # Wake word parameters
                 wakeword_backend: str = "pvporcupine",
                 openwakeword_model_paths: str = None,
                 openwakeword_inference_framework: str = "onnx",
                 wake_words: str = "",
                 wake_words_sensitivity: float = INIT_WAKE_WORDS_SENSITIVITY,
                 wake_word_activation_delay: float = (
                    INIT_WAKE_WORD_ACTIVATION_DELAY
                 ),
                 wake_word_timeout: float = INIT_WAKE_WORD_TIMEOUT,
                 wake_word_buffer_duration: float = INIT_WAKE_WORD_BUFFER_DURATION,
                 on_wakeword_detected=None,
                 on_wakeword_timeout=None,
                 on_wakeword_detection_start=None,
                 on_wakeword_detection_end=None,
                 on_recorded_chunk=None,
                 debug_mode=False,
                 handle_buffer_overflow: bool = INIT_HANDLE_BUFFER_OVERFLOW,
                 beam_size: int = 5,
                 beam_size_realtime: int = 3,
                 buffer_size: int = BUFFER_SIZE,
                 sample_rate: int = SAMPLE_RATE,
                 initial_prompt: Optional[Union[str, Iterable[int]]] = None,
                 suppress_tokens: Optional[List[int]] = [-1],
                 print_transcription_time: bool = False,
                 early_transcription_on_silence: int = 0,
                 allowed_latency_limit: int = ALLOWED_LATENCY_LIMIT,
                 no_log_file: bool = False,
                 use_extended_logging: bool = False,

                 # Server urls
                 control_url: str = DEFAULT_CONTROL_URL,
                 data_url: str = DEFAULT_DATA_URL,
                 autostart_server: bool = True,
                 ):

        # Set instance variables from constructor parameters
        self.model = model
        self.language = language
        self.compute_type = compute_type
        self.input_device_index = input_device_index
        self.gpu_device_index = gpu_device_index
        self.device = device
        self.on_recording_start = on_recording_start
        self.on_recording_stop = on_recording_stop
        self.on_transcription_start = on_transcription_start
        self.ensure_sentence_starting_uppercase = ensure_sentence_starting_uppercase
        self.ensure_sentence_ends_with_period = ensure_sentence_ends_with_period
        self.use_microphone = use_microphone
        self.spinner = spinner
        self.level = level

        # Real-time transcription parameters
        self.enable_realtime_transcription = enable_realtime_transcription
        self.use_main_model_for_realtime = use_main_model_for_realtime
        self.realtime_model_type = realtime_model_type
        self.realtime_processing_pause = realtime_processing_pause
        self.on_realtime_transcription_update = on_realtime_transcription_update
        self.on_realtime_transcription_stabilized = on_realtime_transcription_stabilized

        # Voice activation parameters
        self.silero_sensitivity = silero_sensitivity
        self.silero_use_onnx = silero_use_onnx
        self.silero_deactivity_detection = silero_deactivity_detection
        self.webrtc_sensitivity = webrtc_sensitivity
        self.post_speech_silence_duration = post_speech_silence_duration
        self.min_length_of_recording = min_length_of_recording
        self.min_gap_between_recordings = min_gap_between_recordings
        self.pre_recording_buffer_duration = pre_recording_buffer_duration
        self.on_vad_detect_start = on_vad_detect_start
        self.on_vad_detect_stop = on_vad_detect_stop

        # Wake word parameters
        self.wakeword_backend = wakeword_backend
        self.openwakeword_model_paths = openwakeword_model_paths
        self.openwakeword_inference_framework = openwakeword_inference_framework
        self.wake_words = wake_words
        self.wake_words_sensitivity = wake_words_sensitivity
        self.wake_word_activation_delay = wake_word_activation_delay
        self.wake_word_timeout = wake_word_timeout
        self.wake_word_buffer_duration = wake_word_buffer_duration
        self.on_wakeword_detected = on_wakeword_detected
        self.on_wakeword_timeout = on_wakeword_timeout
        self.on_wakeword_detection_start = on_wakeword_detection_start
        self.on_wakeword_detection_end = on_wakeword_detection_end
        self.on_recorded_chunk = on_recorded_chunk
        self.debug_mode = debug_mode
        self.handle_buffer_overflow = handle_buffer_overflow
        self.beam_size = beam_size
        self.beam_size_realtime = beam_size_realtime
        self.buffer_size = buffer_size
        self.sample_rate = sample_rate
        self.initial_prompt = initial_prompt
        self.suppress_tokens = suppress_tokens
        self.print_transcription_time = print_transcription_time
        self.early_transcription_on_silence = early_transcription_on_silence
        self.allowed_latency_limit = allowed_latency_limit
        self.no_log_file = no_log_file
        self.use_extended_logging = use_extended_logging

        # Server URLs
        self.control_url = control_url
        self.data_url = data_url
        self.autostart_server = autostart_server

        if not self.ensure_server_running():
            print("Cannot start STT server. Exiting.")
            return False
        
        print("STT server is running.")

    def start_server(self):
        args = ['stt-server']

        # Map constructor parameters to server arguments
        if self.model:
            args += ['--model', self.model]
        if self.realtime_model_type:
            args += ['--realtime_model_type', self.realtime_model_type]
        if self.language:
            args += ['--language', self.language]
        if self.silero_sensitivity is not None:
            args += ['--silero_sensitivity', str(self.silero_sensitivity)]
        if self.webrtc_sensitivity is not None:
            args += ['--webrtc_sensitivity', str(self.webrtc_sensitivity)]
        if self.min_length_of_recording is not None:
            args += ['--min_length_of_recording', str(self.min_length_of_recording)]
        if self.min_gap_between_recordings is not None:
            args += ['--min_gap_between_recordings', str(self.min_gap_between_recordings)]
        if self.realtime_processing_pause is not None:
            args += ['--realtime_processing_pause', str(self.realtime_processing_pause)]
        if self.early_transcription_on_silence is not None:
            args += ['--early_transcription_on_silence', str(self.early_transcription_on_silence)]
        if self.beam_size is not None:
            args += ['--beam_size', str(self.beam_size)]
        if self.beam_size_realtime is not None:
            args += ['--beam_size_realtime', str(self.beam_size_realtime)]
        if self.initial_prompt:
            args += ['--initial_prompt', self.initial_prompt]
        if self.control_url:
            parsed_control_url = urlparse(self.control_url)
            if parsed_control_url.port:
                args += ['--control_port', str(parsed_control_url.port)]
        if self.data_url:
            parsed_data_url = urlparse(self.data_url)
            if parsed_data_url.port:
                args += ['--data_port', str(parsed_data_url.port)]

        # Start the subprocess with the mapped arguments
        if os.name == 'nt':  # Windows
            cmd = 'start /min cmd /c ' + subprocess.list2cmdline(args)
            subprocess.Popen(cmd, shell=True)
        else:  # Unix-like systems
            subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        print("STT server start command issued. Please wait a moment for it to initialize.", file=sys.stderr)

    # def start_server(self):
    #     if os.name == 'nt':  # Windows
    #         subprocess.Popen('start /min cmd /c stt-server', shell=True)
    #     else:  # Unix-like systems
    #         subprocess.Popen(['stt-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    #     print("STT server start command issued. Please wait a moment for it to initialize.", file=sys.stderr)

    def is_server_running(self):
        parsed_url = urlparse(self.control_url)
        host = parsed_url.hostname
        port = parsed_url.port or 80
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, port)) == 0

    def ensure_server_running(self):
        if not self.is_server_running():
            print("STT server is not running.", file=sys.stderr)
            if self.autostart_server or self.ask_to_start_server():
                self.start_server()
                print("Waiting for STT server to start...", file=sys.stderr)
                for _ in range(20):  # Wait up to 20 seconds
                    if self.is_server_running():
                        print("STT server started successfully.", file=sys.stderr)
                        time.sleep(2)  # Give the server a moment to fully initialize
                        return True
                    time.sleep(1)
                print("Failed to start STT server.", file=sys.stderr)
                return False
            else:
                print("STT server is required. Please start it manually.", file=sys.stderr)
                return False
        return True

