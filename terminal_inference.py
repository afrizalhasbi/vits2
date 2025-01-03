import os
import numpy as np
import torch
from torch import no_grad, LongTensor
import argparse
import commons
from mel_processing import spectrogram_torch
import utils
from models import SynthesizerTrn
import librosa
import soundfile as sf

from text import text_to_sequence, _clean_text
device = "cuda:0" if torch.cuda.is_available() else "cpu"

language_marks = {
    "Japanese": "",
    "日本語": "[JA]",
    "简体中文": "[ZH]",
    "English": "[EN]",
    "Mix": "",
}
lang = ['日本語', '简体中文', 'English', 'Mix']
def get_text(text, hps, is_symbol):
    text_norm = text_to_sequence(text, hps.symbols, [] if is_symbol else hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = LongTensor(text_norm)
    return text_norm

def create_tts_fn(model, hps, speaker_ids):
    def tts_fn(text, speaker, language, speed):
        if language is not None:
            text = language_marks[language] + text + language_marks[language]
        speaker_id = speaker_ids[speaker]
        stn_tst = get_text(text, hps, False)
        with no_grad():
            x_tst = stn_tst.unsqueeze(0).to(device)
            x_tst_lengths = LongTensor([stn_tst.size(0)]).to(device)
            sid = LongTensor([speaker_id]).to(device)
            audio = model.infer(x_tst, x_tst_lengths, sid=sid, noise_scale=.667, noise_scale_w=0.8,
                                length_scale=1.0 / speed)[0][0, 0].data.cpu().float().numpy()
        del stn_tst, x_tst, x_tst_lengths, sid
        return hps.data.sampling_rate, audio

    return tts_fn

def create_vc_fn(model, hps, speaker_ids):
    def vc_fn(original_speaker, target_speaker, audio_file_path):
        audio, sampling_rate = librosa.load(audio_file_path, sr=None, mono=True)
    
        original_speaker_id = speaker_ids[original_speaker]
        target_speaker_id = speaker_ids[target_speaker]
    
        print(str(audio)[:100])
        audio = (audio / np.finfo(audio.dtype).max).astype(np.float32)
        if len(audio.shape) > 1:
            audio = librosa.to_mono(audio.transpose(1, 0))
        if sampling_rate != hps.data.sampling_rate:
            audio = librosa.resample(audio, orig_sr=sampling_rate, target_sr=hps.data.sampling_rate)
        with no_grad():
            y = torch.FloatTensor(audio)
            y = y / max(-y.min(), y.max()) / 0.99
            y = y.to(device)
            y = y.unsqueeze(0)
            spec = spectrogram_torch(y, hps.data.filter_length,
                                     hps.data.sampling_rate, hps.data.hop_length, hps.data.win_length,
                                     center=False).to(device)
            spec_lengths = LongTensor([spec.size(-1)]).to(device)
            sid_src = LongTensor([original_speaker_id]).to(device)
            sid_tgt = LongTensor([target_speaker_id]).to(device)
            audio = model.voice_conversion(spec, spec_lengths, sid_src=sid_src, sid_tgt=sid_tgt)[0][
                0, 0].data.cpu().float().numpy()
        del y, spec, spec_lengths, sid_src, sid_tgt
        return hps.data.sampling_rate, audio
    return vc_fn

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", default="OUTPUT_MODEL/G_latest.pth", help="directory to your fine-tuned model")
    parser.add_argument("--config_dir", default="configs/modified_finetune_speaker.json", help="directory to your model config file")
    parser.add_argument("--share", default=False, help="make link public (used in colab)")
    parser.add_argument("--src", required=True, help="")
    parser.add_argument("--text", required=True, help="")

    args = parser.parse_args()
    hps = utils.get_hparams_from_file(args.config_dir)


    net_g = SynthesizerTrn(
        len(hps.symbols),
        hps.data.filter_length // 2 + 1,
        hps.train.segment_size // hps.data.hop_length,
        n_speakers=hps.data.n_speakers,
        **hps.model).to(device)
    _ = net_g.eval()

    _ = utils.load_checkpoint(args.model_dir, net_g, None)
    speaker_ids = hps.speakers
    speakers = list(hps.speakers.keys())
    tts_fn = create_tts_fn(net_g, hps, speaker_ids)
    print(f"Available speaker_ids: {speaker_ids}")
    vc_fn = create_vc_fn(net_g, hps, speaker_ids)
    
    sr, audio = tts_fn(args.text, speaker='Surya', language='English', speed=1)
    # sr, audio = vc_fn('Tio', 'Surya', 'tio.mp3')
    sf.write("output.mp3", audio, sr, format="MP3")
    print("Audio saved to output.mp3")


    #-------- comment first --------#

    # args = parser.parse_args()
    # hps = utils.get_hparams_from_file(args.config_dir)

    # net_g = SynthesizerTrn(
    #     len(hps.symbols),
    #     hps.data.filter_length // 2 + 1,
    #     hps.train.segment_size // hps.data.hop_length,
    #     n_speakers=hps.data.n_speakers,
    #     **hps.model
    # ).to(device)
    # _ = net_g.eval()

    # _ = utils.load_checkpoint(args.model_dir, net_g, None)
    # speaker_ids = hps.speakers
    # speakers = list(hps.speakers.keys())
    # tts_fn = create_tts_fn(net_g, hps, speaker_ids)
    # vc_fn = create_vc_fn(net_g, hps, speaker_ids)

    # status, (sr, audio) = tts_fn(
    #     text=args.text, 
    #     speaker=args.src, 
    #     language='Mix',  # or choose from ['日本語','简体中文','English','Mix']
    #     speed=1.0
    # )

    # # Save output to an MP3 file
