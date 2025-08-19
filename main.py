import os
from pydub import AudioSegment
import numpy as np
import librosa
import soundfile as sf

def process_audio(input_path, output_path):
    # 1. 加载音频文件
    audio = AudioSegment.from_file(input_path)
    
    # 2. 轻微调整音频（如音高、速度、噪声）
    samples = np.array(audio.get_array_of_samples())
    sr = audio.frame_rate
    
    # 添加轻微白噪声（0.1%振幅）
    noise = np.random.normal(0, 0.001 * np.max(samples), len(samples))
    samples_processed = samples + noise
    
    # 3. 重新编码并导出（改变比特率、格式）
    processed_audio = AudioSegment(
        samples_processed.tobytes(),
        frame_rate=sr,
        sample_width=audio.sample_width,
        channels=audio.channels
    )
    
    # 4. 保存为不同格式（如WAV → FLAC）
    processed_audio.export(output_path, format="flac", bitrate="192k")

# 批量处理 input_folder 到 output_folder
input_folder = "input"
output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith((".mp3", ".wav", ".flac")):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".flac")
        process_audio(input_path, output_path)
        print(f"Processed: {filename} → {output_path}")
