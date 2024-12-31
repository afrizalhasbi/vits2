pip install --upgrade --force-reinstall regex gradio
pip install imageio==2.4.1
pip install --upgrade youtube-dl moviepy

pip install -r requirements.txt
pip install -U numpy Cython pyzmq librosa soundfile datasets pyopenjtalk unidecode jamo ko_pron pypinyin
pip install --upgrade --force-reinstall numba
pip install pydantic==1.10.4
pip install ruamel.yaml
pip install git+https://github.com/openai/whisper.git

mkdir pretrained_models
wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/D_trilingual.pth -O ./pretrained_models/D_0.pth
wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/pretrained_models/G_trilingual.pth -O ./pretrained_models/G_0.pth
wget https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer/resolve/main/configs/uma_trilingual.json -O ./configs/finetune_speaker.json

wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/sampled_audio4ft_v2.zip
unzip sampled_audio4ft_v2.zip
rm -rf sampled_audio4ft_v2.zip

# build monotonic align
cd monotonic_align
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..

mkdir video_data
mkdir raw_audio
mkdir denoised_audio
mkdir custom_character_voice
mkdir segmented_character_voice
