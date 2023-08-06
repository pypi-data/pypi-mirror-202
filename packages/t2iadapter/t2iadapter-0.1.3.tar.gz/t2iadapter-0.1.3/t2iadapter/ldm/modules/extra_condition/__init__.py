# -*- coding: utf-8 -*-
import torch
from .midas import *
from .openpose import *

from t2iadapter.ldm.modules.extra_condition.utils import load_file_from_url
from t2iadapter.ldm.modules.extra_condition.model_edge import pidinet
from t2iadapter.ldm.modules.extra_condition.midas.api import MiDaSInference
from transformers import CLIPProcessor, CLIPVisionModel
from t2iadapter.ldm.modules.extra_condition.openpose.api import OpenposeInference


def init_sketch_model(model_name, device='cuda'):
    if model_name == 'pidinet':

        # "pidinet"
        model = pidinet()
        model_url = 'https://huggingface.co/TencentARC/T2I-Adapter/blob/main/third-party-models/table5_pidinet.pth'
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    model_path = load_file_from_url(url=model_url, model_dir='~/.cache/t2iadapter', file_name=None)
    state_dict = torch.load(model_path, map_location='cpu')['state_dict']
    model.load_state_dict({k.replace('module.', ''): v for k, v in state_dict.items()}, strict=True)
    model.eval()
    model = model.to(device)
    return model


def init_depth_model(model_name, device='cuda'):
    if model_name == 'midas':

        # "midas"
        model = MiDaSInference(model_type='dpt_hybrid')
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    model.eval()
    model = model.to(device)
    return model


def init_zoedepth_model(model_name, device='cuda'):
    if model_name == 'zoedepth':

        # "zoedepth"
        from handyinfer.depth_estimation import init_depth_estimation_model
        model = init_depth_estimation_model('ZoeD_N', device=device, model_rootpath='/root/.cache/t2iadapter')
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    model.eval()
    model = model.to(device)
    return model


def init_style_model(model_name, device='cuda'):
    if model_name == 'clip-vit-large':

        # "clip-vit-large"
        version = '/root/.cache/t2iadapter/openai/clip-vit-large-patch14'
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')

    processor = CLIPProcessor.from_pretrained(version)
    clip_vision_model = CLIPVisionModel.from_pretrained(version)
    clip_vision_model = clip_vision_model.to(device)
    model = {'processor': processor, 'clip_vision_model': clip_vision_model}
    return model


def init_openpose_model(model_name, device='cuda'):
    if model_name == 'openpose':

        # "openpose"
        model = OpenposeInference()
    else:
        raise NotImplementedError(f'{model_name} is not implemented.')
    model.eval()
    model = model.to(device)
    return model