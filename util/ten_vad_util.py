from ten_vad import TenVad
import numpy as np
from config import *

def getVADScore(
      data_int16: np.array, 
      hop_size: int = VAD_HOP_SIZE, 
      threshold: float = VAD_THRESHOLD, 
      out_prob: bool = False ): 
  
  ten_vad_instance = TenVad(hop_size, threshold)  # Create a TenVad instance
  num_frames = data_int16.shape[0] // hop_size
  # Streaming inference
  total_score = 0
  probs = []
  for i in range(num_frames):
      audio_data = data_int16[i * hop_size: (i + 1) * hop_size]
      out_probability, out_flag = ten_vad_instance.process(audio_data) #  Ou
      if out_prob: probs.append(out_probability)
      total_score += out_flag

  avg_score = total_score/num_frames
  return avg_score, total_score, probs
