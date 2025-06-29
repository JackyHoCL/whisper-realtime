from fastapi import FastAPI, File, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import os
import numpy as np
import argparse
import numpy as np
import io
from client.vllm_client import *
from scipy.io import wavfile
from util.ten_vad_util import *

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

parser = argparse.ArgumentParser(description="Use a specified GPU")
parser.add_argument('--gpu', type=int, default=0, help='GPU index to use')
args = parser.parse_args()

os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)

app = FastAPI()

class TranscriptionResponse(BaseModel):
    language: str
    language_probability: float
    segments: list

@app.websocket("/transcribe/stream")
async def transcribe_stream(ws: WebSocket):
    await ws.accept()
    audio_data_save = bytearray()
    silent_cnt = 0
    recording = False

    try:
        while True:
            data = await ws.receive_bytes()
            await ws.send_json({"transcribing": True})
            data_save_fp32 = np.frombuffer(data, dtype=np.float32)
            data_save_int16 = (data_save_fp32 * 32767).astype(np.int16)
            avg_score, total_score, probs = getVADScore(data_save_int16)

            if (avg_score > VAD_AVG_SCORE_THRESHOLD):
                audio_data_save.extend(data)
                if len(audio_data_save) > VAD_SEND_THRESHOLD:
                    send_to_whisper(audio_data_save)
                    audio_data_save.clear()
                silent_cnt = 0
                recording = True
            else:
                if recording:
                    audio_data_save.extend(data)
                silent_cnt += 1
                if silent_cnt > VAD_SILENT_THRESHOLD and len(audio_data_save) > VAD_MIN_THRESHOLD:
                    send_to_whisper(audio_data_save)
                    audio_data_save.clear()
                    recording = False

    except WebSocketDisconnect:
        print("Client disconnected")

def send_to_whisper(audio_data_save):
    data_save_fp32 = np.frombuffer(audio_data_save, dtype=np.float32)
    data_save_int16 = (data_save_fp32 * 32767).astype(np.int16)

    byte_buffer = io.BytesIO()
    wavfile.write(byte_buffer, rate=AUDIO_SAMPLE_RATE, data=data_save_int16)
    byte_buffer.seek(0)
    buffered_reader = io.BufferedReader(byte_buffer)
    sync_openai(buffered_reader)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('server:app', host=SERVER_HOST, port=SERVER_PORT, reload=SERVER_RELOAD)