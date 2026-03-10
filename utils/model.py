import os
import json

import torch
import numpy as np

import hifigan
from model import FastSpeech2, ScheduledOptim


def get_model(args, configs, device, train=False):
    (preprocess_config, model_config, train_config) = configs

    model = FastSpeech2(preprocess_config, model_config).to(device)
    if args.restore_step:
        ckpt_path = os.path.join(
            train_config["path"]["ckpt_path"],
            "{}.pth.tar".format(args.restore_step),
        )
        ckpt = torch.load(ckpt_path, weights_only=False)
        model.load_state_dict(ckpt["model"])

    if train:
        scheduled_optim = ScheduledOptim(
            model, train_config, model_config, args.restore_step
        )
        if args.restore_step:
            scheduled_optim.load_state_dict(ckpt["optimizer"])
        model.train()
        return model, scheduled_optim

    model.eval()
    model.requires_grad_ = False
    return model


def get_param_num(model):
    num_param = sum(param.numel() for param in model.parameters())
    return num_param


def get_vocoder(model_config, device):
    import json
    import sys
    
    # Add hifigan to path
    hifigan_path = os.path.join(os.path.dirname(__file__), "..", "hifigan")
    sys.path.insert(0, hifigan_path)
    
    from hifigan import AttrDict
    from hifigan.models import Generator
    
    # Load config
    config_path = os.path.join(os.path.dirname(__file__), "..", "hifigan", "config.json")
    with open(config_path) as f:
        h = AttrDict(json.load(f))
    
    # Load checkpoint
    checkpoint_path = os.path.join(os.path.dirname(__file__), "..", "hifigan", "generator_universal.pth.tar")
    
    # Initialize generator
    vocoder = Generator(h).to(device)
    
    # Load state dict with device mapping
    ckpt = torch.load(checkpoint_path, map_location=device)
    vocoder.load_state_dict(ckpt['generator'])
    vocoder.eval()
    vocoder.remove_weight_norm()
    
    return vocoder

def vocoder_infer(mels, vocoder, model_config, preprocess_config, lengths=None):
    name = model_config["vocoder"]["model"]
    with torch.no_grad():
        if name == "MelGAN":
            wavs = vocoder.inverse(mels / np.log(10))
        elif name == "HiFi-GAN":
            wavs = vocoder(mels).squeeze(1)

    wavs = (
        wavs.cpu().numpy()
        * preprocess_config["preprocessing"]["audio"]["max_wav_value"]
    ).astype("int16")
    wavs = [wav for wav in wavs]

    for i in range(len(mels)):
        if lengths is not None:
            wavs[i] = wavs[i][: lengths[i]]

    return wavs
