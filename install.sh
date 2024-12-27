pip install --upgrade --force-reinstall regex soundfile gradio
pip install imageio==2.4.1
pip install --upgrade youtube-dl moviepy

pip install --no-build-isolation -r requirements.txt
pip install -U numpy Cython pyzmq
pip install --upgrade --force-reinstall numba
pip install pydantic==1.10.4
pip install ruamel.yaml
pip install git+https://github.com/openai/whisper.git

# build monotonic align
cd monotonic_align/
mkdir monotonic_align
python setup.py build_ext --inplace
cd ..
mkdir pretrained_models
# download data for fine-tuning
# create necessary directories
mkdir video_data
mkdir raw_audio
mkdir denoised_audio
mkdir custom_character_voice
mkdir segmented_character_voice
