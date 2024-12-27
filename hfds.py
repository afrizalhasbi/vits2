from tqdm import tqdm
from datasets import load_dataset
import os
import sys

assert len(sys.argv) > 1, "Please provide dataset name as command line argument"
ds_name = sys.argv[1]
ds = load_dataset(ds_name)['train']
output_dir = ds_name.split("/")[-1]
os.makedirs(output_dir, exist_ok=True)
txt_output = ""
for i, item in tqdm(enumerate(ds), total=len(ds)):  # or your specific split
    audio_data = item['audio']
    audio_path = os.path.join(output_dir, f"{i}.mp3")
    
    if isinstance(audio_data, dict):  # if audio is in array format
        import soundfile as sf
        sf.write(audio_path, audio_data['array'], audio_data['sampling_rate'])
    else:  # if audio is already a file path
        import shutil
        shutil.copy(audio_data, audio_path)
    txt.append(f"{audio_path}|{output_dir}|[LANG]EN[LANG]")
