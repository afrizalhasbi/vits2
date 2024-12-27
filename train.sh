python scripts/resample.py
python preprocess_v2.py --add_auxiliary_data True --languages
python finetune_speaker_v2.py -m ./OUTPUT_MODEL --max_epochs "10" --drop_speaker_embed True
