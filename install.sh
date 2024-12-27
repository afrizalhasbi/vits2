python -m pip install --upgrade --force-reinstall regex
python -m pip install --force-reinstall soundfile
python -m pip install --force-reinstall gradio
python -m pip install imageio==2.4.1
python -m pip install --upgrade youtube-dl
python -m pip install moviepy

python -m pip install --no-build-isolation -r requirements.txt
python -m pip install --upgrade numpy
python -m pip install --upgrade --force-reinstall numba
python -m pip install --upgrade Cython

python -m pip install --upgrade pyzmq
python -m pip install pydantic==1.10.4
python -m pip install ruamel.yaml
python -m pip install git+https://github.com/openai/whisper.git

# build monotonic align
cd monotonic_align/
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
mkdir pretrained_models
# download data for fine-tuning
wget https://huggingface.co/datasets/Plachta/sampled_audio4ft/resolve/main/sampled_audio4ft_v2.zip
unzip sampled_audio4ft_v2.zip
# create necessary directories
mkdir video_data
mkdir raw_audio
mkdir denoised_audio
mkdir custom_character_voice
mkdir segmented_character_voice
