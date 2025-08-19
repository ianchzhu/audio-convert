import os
import numpy as np
from pydub import AudioSegment
import random

def process_audio(input_path, output_path):
    """
    处理音频文件以绕过AI检测
    """
    try:
        # 1. 加载音频文件
        audio = AudioSegment.from_file(input_path)
        
        # 2. 转换为numpy数组进行处理
        samples = np.array(audio.get_array_of_samples())
        
        # 3. 应用多种处理技术
        # a. 添加轻微随机噪声 (0.05% 振幅)
        noise_amplitude = 0.0005 * np.max(np.abs(samples))
        noise = np.random.normal(0, noise_amplitude, len(samples))
        samples = samples.astype(np.float32) + noise
        
        # b. 轻微随机音高偏移 (±1%)
        pitch_shift = random.uniform(0.99, 1.01)
        if len(samples) > 1000:  # 确保有足够样本
            from scipy import signal  # 局部导入，避免依赖问题
            samples = signal.resample(samples, int(len(samples) * pitch_shift))
        
        # c. 轻微音量变化 (±3%)
        volume_factor = random.uniform(0.97, 1.03)
        samples = samples * volume_factor
        
        # 4. 转换回整数格式
        samples = np.clip(samples, -32768, 32767).astype(np.int16)
        
        # 5. 创建新的音频段
        processed_audio = AudioSegment(
            samples.tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
        
        # 6. 导出为不同格式（改变文件特征）
        # 使用中等比特率，避免过高或过低
        processed_audio.export(output_path, format="wav", bitrate="192k")
        
        return True
        
    except Exception as e:
        print(f"处理 {input_path} 时出错: {str(e)}")
        return False

def simple_process_audio(input_path, output_path):
    """
    简化版处理（不依赖scipy）
    """
    try:
        # 1. 加载音频文件
        audio = AudioSegment.from_file(input_path)
        
        # 2. 转换为numpy数组
        samples = np.array(audio.get_array_of_samples())
        
        # 3. 简单处理 - 只添加噪声和音量变化
        # a. 添加轻微随机噪声
        noise_amplitude = 0.0003 * np.max(np.abs(samples))
        noise = np.random.normal(0, noise_amplitude, len(samples))
        samples = samples.astype(np.float32) + noise
        
        # b. 轻微音量变化
        volume_factor = random.uniform(0.98, 1.02)
        samples = samples * volume_factor
        
        # 4. 转换回整数格式
        samples = np.clip(samples, -32768, 32767).astype(np.int16)
        
        # 5. 创建新的音频段
        processed_audio = AudioSegment(
            samples.tobytes(),
            frame_rate=audio.frame_rate,
            sample_width=audio.sample_width,
            channels=audio.channels
        )
        
        # 6. 导出为FLAC格式
        processed_audio.export(output_path, format="wav")
        
        return True
        
    except Exception as e:
        print(f"处理 {input_path} 时出错: {str(e)}")
        return False

# 批量处理函数
def batch_process_audio(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    processed_count = 0
    total_count = 0
    
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.mp3', '.wav', '.flac', '.m4a', '.aac')):
            total_count += 1
            input_path = os.path.join(input_folder, filename)
            name, ext = os.path.splitext(filename)
            output_path = os.path.join(output_folder, f"{name}.wav")
            
            print(f"正在处理: {filename}")
            
            # 尝试使用简化版处理
            if simple_process_audio(input_path, output_path):
                processed_count += 1
                print(f"✓ 完成: {filename} → {name}.wav")
            else:
                print(f"✗ 失败: {filename}")
    
    print(f"\n处理完成: {processed_count}/{total_count} 个文件成功")

# 使用示例
if __name__ == "__main__":
    input_folder = "input"  # 输入文件夹
    output_folder = "output"  # 输出文件夹
    
    batch_process_audio(input_folder, output_folder)
