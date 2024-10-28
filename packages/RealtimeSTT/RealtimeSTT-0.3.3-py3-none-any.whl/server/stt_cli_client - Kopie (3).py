import os
import sys
import pyaudio
import numpy as np
from scipy import signal
import logging
os.environ['ALSA_LOG_LEVEL'] = 'none'

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Default fallback rate
input_device_index = None
audio_interface = None
stream = None
device_sample_rate = None
chunk_size = CHUNK

def get_highest_sample_rate(audio_interface, device_index):
    """Get the highest supported sample rate for the specified device."""
    try:
        device_info = audio_interface.get_device_info_by_index(device_index)
        max_rate = int(device_info['defaultSampleRate'])

        if 'supportedSampleRates' in device_info:
            supported_rates = [int(rate) for rate in device_info['supportedSampleRates']]
            if supported_rates:
                max_rate = max(supported_rates)

        return max_rate
    except Exception as e:
        logging.warning(f"Failed to get highest sample rate: {e}")
        return 48000  # Fallback to a common high sample rate

def initialize_audio_stream(audio_interface, device_index, sample_rate, chunk_size):
    """Initialize the audio stream with error handling."""
    try:
        stream = audio_interface.open(
            format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size,
            input_device_index=device_index,
        )
        return stream
    except Exception as e:
        logging.error(f"Error initializing audio stream: {e}")
        raise

def preprocess_audio(chunk, original_sample_rate, target_sample_rate):
    """Preprocess audio chunk similar to feed_audio method."""
    if isinstance(chunk, np.ndarray):
        if chunk.ndim == 2:  # Stereo to mono conversion
            chunk = np.mean(chunk, axis=1)

        # Resample if needed
        if original_sample_rate != target_sample_rate:
            num_samples = int(len(chunk) * target_sample_rate / original_sample_rate)
            chunk = signal.resample(chunk, num_samples)

        chunk = chunk.astype(np.int16)
    else:
        chunk = np.frombuffer(chunk, dtype=np.int16)

        if original_sample_rate != target_sample_rate:
            num_samples = int(len(chunk) * target_sample_rate / original_sample_rate)
            chunk = signal.resample(chunk, num_samples)
            chunk = chunk.astype(np.int16)

    return chunk.tobytes()

def setup_audio():
    global audio_interface, stream, device_sample_rate, input_device_index
    try:
        audio_interface = pyaudio.PyAudio()
        if input_device_index is None:
            try:
                default_device = audio_interface.get_default_input_device_info()
                input_device_index = default_device['index']
            except OSError as e:
                input_device_index = None

        sample_rates_to_try = [16000]  # Try 16000 Hz first
        if input_device_index is not None:
            highest_rate = get_highest_sample_rate(audio_interface, input_device_index)
            if highest_rate != 16000:
                sample_rates_to_try.append(highest_rate)
        else:
            sample_rates_to_try.append(48000)  # Fallback sample rate

        for rate in sample_rates_to_try:
            try:
                device_sample_rate = rate
                stream = initialize_audio_stream(audio_interface, input_device_index, device_sample_rate, chunk_size)
                if stream is not None:
                    logging.debug(f"Audio recording initialized successfully at {device_sample_rate} Hz, reading {chunk_size} frames at a time")
                    return True
            except Exception as e:
                logging.warning(f"Failed to initialize audio stream at {device_sample_rate} Hz: {e}")
                continue

        raise Exception("Failed to initialize audio stream with all sample rates.")
    except Exception as e:
        logging.exception(f"Error initializing audio recording: {e}")
        if audio_interface:
            audio_interface.terminate()
        return False

from .install_packages import check_and_install_packages

check_and_install_packages([
    {
        'module_name': 'websocket',                    # Import module
        'install_name': 'websocket-client',            # Package name for pip install
    },
    {
        'module_name': 'pyaudio',                      # Import module
        'install_name': 'pyaudio',                     # Package name for pip install
    },
    {
        'module_name': 'colorama',                     # Import module
        'attribute': 'init',                           # Attribute to check (init method from colorama)
        'install_name': 'colorama',                    # Package name for pip install
        'version': '',                                 # Optional version constraint
    },
])

import websocket
import pyaudio
from colorama import init, Fore, Style

import argparse
import json
import threading
import time
import struct
import socket
import subprocess
import shutil
from urllib.parse import urlparse
from queue import Queue

# Initialize colorama
init()

# Constants
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DEFAULT_SERVER_URL = "ws://localhost:8011"

class STTWebSocketClient:
    def __init__(self, server_url, debug=False, file_output=None, norealtime=False):
        self.server_url = server_url
        self.ws = None
        self.is_running = False
        self.debug = debug
        self.file_output = file_output
        self.last_text = ""
        self.pbar = None
        self.console_width = shutil.get_terminal_size().columns
        self.recording_indicator = "🔴"
        self.norealtime = norealtime
        self.connection_established = threading.Event()
        self.message_queue = Queue()
        self.commands = Queue()
        self.stop_event = threading.Event()

    def debug_print(self, message):
        if self.debug:
            print(message, file=sys.stderr)

    def connect(self):
        if not self.ensure_server_running():
            self.debug_print("Cannot start STT server. Exiting.")
            return False

        websocket.enableTrace(self.debug)
        try:
            self.ws = websocket.WebSocketApp(self.server_url,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close,
                                             on_open=self.on_open)
            
            self.ws_thread = threading.Thread(target=self.ws.run_forever)
            self.ws_thread.daemon = True
            self.ws_thread.start()

            # Wait for the connection to be established
            if not self.connection_established.wait(timeout=10):
                self.debug_print("Timeout while connecting to the server.")
                return False
            
            self.debug_print("WebSocket connection established successfully.")
            return True
        except Exception as e:
            self.debug_print(f"Error while connecting to the server: {e}")
            return False

    def on_open(self, ws):
        self.debug_print("WebSocket connection opened.")
        self.is_running = True
        self.connection_established.set()
        self.start_recording()
        self.start_command_processor()

    def on_error(self, ws, error):
        self.debug_print(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        self.debug_print(f"WebSocket connection closed: {close_status_code} - {close_msg}")
        self.is_running = False
        self.stop_event.set()

    def is_server_running(self):
        parsed_url = urlparse(self.server_url)
        host = parsed_url.hostname
        port = parsed_url.port or 80
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex((host, port)) == 0

    def ask_to_start_server(self):
        response = input("Would you like to start the STT server now? (y/n): ").strip().lower()
        return response == 'y' or response == 'yes'

    def start_server(self):
        if os.name == 'nt':  # Windows
            subprocess.Popen('start /min cmd /c stt-server', shell=True)
        else:  # Unix-like systems
            subprocess.Popen(['stt-server'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        print("STT server start command issued. Please wait a moment for it to initialize.", file=sys.stderr)

    def ensure_server_running(self):
        if not self.is_server_running():
            print("STT server is not running.", file=sys.stderr)
            if self.ask_to_start_server():
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

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            
            # Handle real-time transcription updates
            if data.get('type') == 'realtime':
                if data['text'] != self.last_text:
                    self.last_text = data['text']
                    if not self.norealtime:
                        self.update_progress_bar(self.last_text) 
            
            # Handle full sentences
            elif data.get('type') == 'fullSentence':
                if self.file_output:
                    sys.stderr.write('\r\033[K')
                    sys.stderr.write(data['text'])
                    sys.stderr.write('\n')
                    sys.stderr.flush()
                    print(data['text'], file=self.file_output)
                    self.file_output.flush()  # Ensure it's written immediately
                else:
                    self.finish_progress_bar()
                    print(f"{data['text']}")
                self.stop()
            
            # Handle server response with status
            elif 'status' in data:
                if data['status'] == 'success':
                    print(f"Server Response: {data.get('message', '')}")
                    if 'parameter' in data and 'value' in data:
                        print(f"Parameter {data['parameter']} = {data['value']}")
                elif data['status'] == 'error':
                    print(f"Server Error: {data.get('message', '')}")
            else:
                self.debug_print(f"Unknown message format: {data}")
        
        except json.JSONDecodeError:
            self.debug_print(f"Received non-JSON message: {message}")
        except Exception as e:
            self.debug_print(f"Error processing message: {e}")


    # def on_message(self, ws, message):
    #     try:
    #         data = json.loads(message)
    #         if data['type'] == 'realtime':
    #             if data['text'] != self.last_text:
    #                 self.last_text = data['text']
    #                 if not self.norealtime:
    #                     self.update_progress_bar(self.last_text) 
    #         elif data['type'] == 'fullSentence':
    #             if self.file_output:
    #                 sys.stderr.write('\r\033[K')
    #                 sys.stderr.write(data['text'])
    #                 sys.stderr.write('\n')
    #                 sys.stderr.flush()
    #                 print(data['text'], file=self.file_output)
    #                 self.file_output.flush()  # Ensure it's written immediately
    #             else:
    #                 self.finish_progress_bar()
    #                 print(f"{data['text']}")        
    #             self.stop()
    #         elif data['status'] == 'success':
    #             print(f"Server Response: {data.get('message', '')}")
    #             if 'parameter' in data and 'value' in data:
    #                 print(f"Parameter {data['parameter']} = {data['value']}")
    #         elif data['status'] == 'error':
    #             print(f"Server Error: {data.get('message', '')}")
    #     except json.JSONDecodeError:
    #         self.debug_print(f"\nReceived non-JSON message: {message}")

    def show_initial_indicator(self):
        if self.norealtime:
            return

        initial_text = f"{self.recording_indicator}\b\b"
        sys.stderr.write(initial_text)
        sys.stderr.flush()

    def update_progress_bar(self, text):
        # Reserve some space for the progress bar decorations
        available_width = self.console_width - 5
        
        # Clear the current line
        sys.stderr.write('\r\033[K')  # Move to the beginning of the line and clear it

        # Get the last 'available_width' characters, but don't cut words
        words = text.split()
        last_chars = ""
        for word in reversed(words):
            if len(last_chars) + len(word) + 1 > available_width:
                break
            last_chars = word + " " + last_chars

        last_chars = last_chars.strip()

        # Color the text yellow and add recording indicator
        colored_text = f"{Fore.YELLOW}{last_chars}{Style.RESET_ALL}{self.recording_indicator}\b\b"

        sys.stderr.write(colored_text)
        sys.stderr.flush()

    def finish_progress_bar(self):
        # Clear the current line
        sys.stderr.write('\r\033[K')
        sys.stderr.flush()

    def stop(self):
        self.finish_progress_bar()
        self.is_running = False
        self.stop_event.set()
        if self.ws:
            self.ws.close()

    def start_recording(self):
        threading.Thread(target=self.record_and_send_audio).start()

    def record_and_send_audio(self):
        if not setup_audio():
            raise Exception("Failed to set up audio recording.")

        self.debug_print("Recording and sending audio...")
        self.show_initial_indicator()

        while self.is_running:
            try:
                self.debug_print("SEEEND1")
                audio_data = stream.read(CHUNK)
                self.debug_print("SEEEND2")

                # Prepare metadata
                metadata = {
                    "sampleRate": device_sample_rate
                }
                metadata_json = json.dumps(metadata)
                metadata_length = len(metadata_json)

                # Construct the message
                message = struct.pack('<I', metadata_length) + metadata_json.encode('utf-8') + audio_data

                self.ws.send(message, opcode=websocket.ABNF.OPCODE_BINARY)

            except Exception as e:
                self.debug_print(f"Error sending audio data: {e}")
                break

        print(f"self.is_running: {self.is_running}")
        self.debug_print("Stopped recording.")
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()

    # New methods to send commands to the server
    def set_parameter(self, parameter, value):
        command = {
            "command": "set_parameter",
            "parameter": parameter,
            "value": value
        }
        self.ws.send(json.dumps(command))

    def get_parameter(self, parameter):
        command = {
            "command": "get_parameter",
            "parameter": parameter
        }
        self.ws.send(json.dumps(command))

    def call_method(self, method, args=None, kwargs=None):
        command = {
            "command": "call_method",
            "method": method,
            "args": args or [],
            "kwargs": kwargs or {}
        }
        self.ws.send(json.dumps(command))

    def start_command_processor(self):
        threading.Thread(target=self.command_processor).start()

    def command_processor(self):
        while self.is_running and not self.stop_event.is_set():
            try:
                # Fetch command from queue if available
                try:
                    command = self.commands.get(timeout=0.1)
                except:
                    command = None

                if command:
                    if command['type'] == 'set_parameter':
                        self.set_parameter(command['parameter'], command['value'])
                    elif command['type'] == 'get_parameter':
                        self.get_parameter(command['parameter'])
                    elif command['type'] == 'call_method':
                        self.call_method(command['method'], command.get('args'), command.get('kwargs'))
                else:
                    time.sleep(0.1)
            except Exception as e:
                self.debug_print(f"Error in command processor: {e}")

    def add_command(self, command):
        self.commands.put(command)

def main():
    parser = argparse.ArgumentParser(description="STT Client")
    parser.add_argument("--server", default=DEFAULT_SERVER_URL, help="STT WebSocket server URL")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-nort", "--norealtime", action="store_true", help="Disable real-time output")
    parser.add_argument("--set-param", nargs=2, metavar=('PARAM', 'VALUE'), action='append',
                        help="Set a recorder parameter. Can be used multiple times.")
    parser.add_argument("--call-method", nargs='+', metavar='METHOD', action='append',
                        help="Call a recorder method with optional arguments.")
    parser.add_argument("--get-param", nargs=1, metavar='PARAM', action='append',
                        help="Get the value of a recorder parameter. Can be used multiple times.")
    args = parser.parse_args()

    # Check if output is being redirected
    if not os.isatty(sys.stdout.fileno()):
        file_output = sys.stdout
    else:
        file_output = None
    
    client = STTWebSocketClient(args.server, args.debug, file_output, args.norealtime)
  
    def signal_handler(sig, frame):
        client.stop()
        sys.exit(0)

    import signal
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        if client.connect():
            # Process command-line parameters
            if args.set_param:
                for param, value in args.set_param:
                    try:
                        # Attempt to parse the value to the appropriate type
                        if '.' in value:
                            value = float(value)
                        else:
                            value = int(value)
                    except ValueError:
                        pass  # Keep as string if not a number

                    client.add_command({
                        'type': 'set_parameter',
                        'parameter': param,
                        'value': value
                    })

            if args.get_param:
                for param_list in args.get_param:
                    param = param_list[0]
                    client.add_command({
                        'type': 'get_parameter',
                        'parameter': param
                    })

            if args.call_method:
                for method_call in args.call_method:
                    method = method_call[0]
                    args_list = method_call[1:] if len(method_call) > 1 else []
                    client.add_command({
                        'type': 'call_method',
                        'method': method,
                        'args': args_list
                    })

            # If command-line parameters were used (like --get-param), wait for them to be processed
            if args.set_param or args.get_param or args.call_method:
                while not client.commands.empty():
                    time.sleep(0.1)
                # If no further commands, continue with audio recording
                client.start_recording()
            else:
                # Start recording directly if no command-line params were provided
                print("Connection established. Recording... (Press Ctrl+C to stop)", file=sys.stderr)
                while client.is_running:
                    time.sleep(0.1)

        else:
            print("Failed to connect to the server.", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.stop()


# def main():
#     parser = argparse.ArgumentParser(description="STT Client")
#     parser.add_argument("--server", default=DEFAULT_SERVER_URL, help="STT WebSocket server URL")
#     parser.add_argument("--debug", action="store_true", help="Enable debug mode")
#     parser.add_argument("-nort", "--norealtime", action="store_true", help="Disable real-time output")    
#     parser.add_argument("--set-param", nargs=2, metavar=('PARAM', 'VALUE'), action='append',
#                         help="Set a recorder parameter. Can be used multiple times.")
#     parser.add_argument("--call-method", nargs='+', metavar='METHOD', action='append',
#                         help="Call a recorder method with optional arguments.")
#     parser.add_argument("--get-param", nargs=1, metavar='PARAM', action='append',
#                         help="Get the value of a recorder parameter. Can be used multiple times.")
#     args = parser.parse_args()

#     # Check if output is being redirected
#     if not os.isatty(sys.stdout.fileno()):
#         file_output = sys.stdout
#     else:
#         file_output = None
    
#     client = STTWebSocketClient(args.server, args.debug, file_output, args.norealtime)
  
#     def signal_handler(sig, frame):
#         client.stop()
#         sys.exit(0)

#     import signal
#     signal.signal(signal.SIGINT, signal_handler)
    
#     try:
#         if client.connect():
#             # Process command-line parameters
#             if args.set_param:
#                 for param, value in args.set_param:
#                     try:
#                         # Attempt to parse the value to the appropriate type
#                         if '.' in value:
#                             value = float(value)
#                         else:
#                             value = int(value)
#                     except ValueError:
#                         pass  # Keep as string if not a number

#                     client.add_command({
#                         'type': 'set_parameter',
#                         'parameter': param,
#                         'value': value
#                     })

#             if args.get_param:
#                 for param_list in args.get_param:
#                     param = param_list[0]
#                     client.add_command({
#                         'type': 'get_parameter',
#                         'parameter': param
#                     })

#             if args.call_method:
#                 for method_call in args.call_method:
#                     method = method_call[0]
#                     args_list = method_call[1:] if len(method_call) > 1 else []
#                     client.add_command({
#                         'type': 'call_method',
#                         'method': method,
#                         'args': args_list
#                     })

#             # Interactive mode
#             if not (args.set_param or args.get_param or args.call_method):
#                 print("Connection established. Recording... (Press Ctrl+C to stop)", file=sys.stderr)
#                 while client.is_running:
#                     time.sleep(0.1)
#             else:
#                 # Wait for commands to be processed
#                 while not client.commands.empty():
#                     time.sleep(0.1)
#                 client.stop()
#         else:
#             print("Failed to connect to the server.", file=sys.stderr)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         client.stop()

# if __name__ == "__main__":
#     main()
