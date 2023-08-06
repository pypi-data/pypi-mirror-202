from enum import Enum, unique

import cv2
import torch
from basicsr.utils import img2tensor
from t2iadapter.ldm.util import resize_numpy_image
from PIL import Image
from torch import autocast


@unique
class ExtraCondition(Enum):
    sketch = 0
    seg = 2
    depth = 3
    canny = 4
    style = 5
    color = 6
    openpose = 7
    zoedepth = 8


def get_cond_model(opt, cond_type: ExtraCondition):
    if cond_type == ExtraCondition.sketch:
        from t2iadapter.ldm.modules.extra_condition import init_sketch_model
        model = init_sketch_model(model_name='pidinet', device=opt.device)
        return model
    elif cond_type == ExtraCondition.seg:
        raise NotImplementedError
    elif cond_type == ExtraCondition.depth:
        from t2iadapter.ldm.modules.extra_condition import init_depth_model
        model = init_depth_model(model_name='midas', device=opt.device)
        return model
    elif cond_type == ExtraCondition.zoedepth:
        from t2iadapter.ldm.modules.extra_condition import init_zoedepth_model
        model = init_zoedepth_model(model_name='zoedepth', device=opt.device)
        return model
    elif cond_type == ExtraCondition.canny:
        return None
    elif cond_type == ExtraCondition.style:
        from t2iadapter.ldm.modules.extra_condition import init_style_model
        model = init_style_model(model_name='clip-vit-large', device=opt.device)
        return model
    elif cond_type == ExtraCondition.color:
        return None
    elif cond_type == ExtraCondition.openpose:
        from t2iadapter.ldm.modules.extra_condition import init_openpose_model
        model = init_openpose_model(model_name='openpose', device=opt.device)
        return model
    else:
        raise NotImplementedError


def get_cond_sketch(opt, cond_image, cond_inp_type, cond_model=None):
    if isinstance(cond_image, str):
        edge = cv2.imread(cond_image)
    else:
        # for gradio input, pay attention, it's rgb numpy
        edge = cv2.cvtColor(cond_image, cv2.COLOR_RGB2BGR)
    edge = resize_numpy_image(edge, max_resolution=opt.max_resolution, resize_short_edge=opt.resize_short_edge)
    opt.H, opt.W = edge.shape[:2]
    if cond_inp_type == 'sketch':
        edge = img2tensor(edge)[0].unsqueeze(0).unsqueeze(0) / 255.
        edge = edge.to(opt.device)
    elif cond_inp_type == 'image':
        edge = img2tensor(edge).unsqueeze(0) / 255.
        edge = cond_model(edge.to(opt.device))[-1]
    else:
        raise NotImplementedError

    # edge = 1-edge # for white background
    edge = edge > 0.5
    edge = edge.float()

    return edge


def get_cond_seg(opt, cond_image, cond_inp_type='image', cond_model=None):
    if isinstance(cond_image, str):
        seg = cv2.imread(cond_image)
    else:
        seg = cv2.cvtColor(cond_image, cv2.COLOR_RGB2BGR)
    seg = resize_numpy_image(seg, max_resolution=opt.max_resolution, resize_short_edge=opt.resize_short_edge)
    opt.H, opt.W = seg.shape[:2]
    if cond_inp_type == 'seg':
        seg = img2tensor(seg).unsqueeze(0) / 255.
        seg = seg.to(opt.device)
    else:
        raise NotImplementedError

    return seg


def get_cond_keypose(opt, cond_image, cond_inp_type='image', cond_model=None):
    if isinstance(cond_image, str):
        pose = cv2.imread(cond_image)
    else:
        pose = cv2.cvtColor(cond_image, cv2.COLOR_RGB2BGR)
    pose = resize_numpy_image(pose, max_resolution=opt.max_resolution, resize_short_edge=opt.resize_short_edge)
    opt.H, opt.W = pose.shape[:2]
    if cond_inp_type == 'keypose':
        pose = img2tensor(pose).unsqueeze(0) / 255.
        pose = pose.to(opt.device)
    else:
        raise NotImplementedError

    return pose


def get_cond_depth(opt, cond_image, cond_inp_type='image', cond_model=None):
    if isinstance(cond_image, str):
        depth = cv2.imread(cond_image)
    else:
        depth = cv2.cvtColor(cond_image, cv2.COLOR_RGB2BGR)
    depth = resize_numpy_image(depth, max_resolution=opt.max_resolution, resize_short_edge=opt.resize_short_edge)
    opt.H, opt.W = depth.shape[:2]
    if cond_inp_type == 'depth':
        depth = img2tensor(depth).unsqueeze(0) / 255.
        depth = depth.to(opt.device)
    elif cond_inp_type == 'image':
        depth = img2tensor(depth).unsqueeze(0) / 127.5 - 1.0
        depth = cond_model(depth.to(opt.device)).repeat(1, 3, 1, 1)
        depth -= torch.min(depth)
        depth /= torch.max(depth)
    else:
        raise NotImplementedError

    return depth


def get_cond_zoedepth(opt, cond_image, cond_inp_type='image', cond_model=None):
    if isinstance(cond_image, str):
        depth = cv2.imread(cond_image)
    else:
        depth = cv2.cvtColor(cond_image, cv2.COLOR_RGB2BGR)
    depth = resize_numpy_image(depth, max_resolution=opt.max_resolution, resize_short_edge=opt.resize_short_edge)
    opt.H, opt.W = depth.shape[:2]
    if cond_inp_type == 'zoedepth':
        depth = img2tensor(depth).unsqueeze(0) / 255.
        depth = depth.to(opt.device)
    elif cond_inp_type == 'image':
        depth = img2tensor(depth).unsqueeze(0) / 255.

        with autocast("cuda", dtype=torch.float32):
            depth = cond_model.infer(depth.to(opt.device))
        depth = depth.repeat(1, 3, 1, 1)
    else:
        raise NotImplementedError

    return depth


def get_cond_canny(opt, cond_image, cond_inp_type='image', cond_model=None):
    if isinstance(cond_image, str):
        canny = cv2.imread(cond_image)
    else:
        canny = cv2.cvtColor(cond_image, cv2.COLOR_RGB2BGR)
    canny = resize_numpy_image(canny, max_resolution=opt.max_resolution, resize_short_edge=opt.resize_short_edge)
    opt.H, opt.W = canny.shape[:2]
    if cond_inp_type == 'canny':
        canny = img2tensor(canny)[0:1].unsqueeze(0) / 255.
        canny = canny.to(opt.device)
    elif cond_inp_type == 'image':
        canny = cv2.Canny(canny, 100, 200)[..., None]
        canny = img2tensor(canny).unsqueeze(0) / 255.
        canny = canny.to(opt.device)
    else:
        raise NotImplementedError

    return canny


def get_cond_style(opt, cond_image, cond_inp_type='image', cond_model=None):
    assert cond_inp_type == 'image'
    if isinstance(cond_image, str):
        style = Image.open(cond_image)
    else:
        # numpy image to PIL image
        style = Image.fromarray(cond_image)

    style_for_clip = cond_model['processor'](images=style, return_tensors="pt")['pixel_values']
    style_feat = cond_model['clip_vision_model'](style_for_clip.to(opt.device))['last_hidden_state']

    return style_feat


def get_cond_color(opt, cond_image, cond_inp_type='image', cond_model=None):
    if isinstance(cond_image, str):
        color = cv2.imread(cond_image)
    else:
        color = cv2.cvtColor(cond_image, cv2.COLOR_RGB2BGR)
    color = resize_numpy_image(color, max_resolution=opt.max_resolution, resize_short_edge=opt.resize_short_edge)
    opt.H, opt.W = color.shape[:2]
    if cond_inp_type == 'image':
        color = cv2.resize(color, (opt.W // 64, opt.H // 64), interpolation=cv2.INTER_CUBIC)
        color = cv2.resize(color, (opt.W, opt.H), interpolation=cv2.INTER_NEAREST)
    color = img2tensor(color).unsqueeze(0) / 255.
    color = color.to(opt.device)
    return color


def get_cond_openpose(opt, cond_image, cond_inp_type='image', cond_model=None):
    if isinstance(cond_image, str):
        openpose_keypose = cv2.imread(cond_image)
    else:
        openpose_keypose = cv2.cvtColor(cond_image, cv2.COLOR_RGB2BGR)
    openpose_keypose = resize_numpy_image(
        openpose_keypose, max_resolution=opt.max_resolution, resize_short_edge=opt.resize_short_edge)
    opt.H, opt.W = openpose_keypose.shape[:2]
    if cond_inp_type == 'openpose':
        openpose_keypose = img2tensor(openpose_keypose).unsqueeze(0) / 255.
        openpose_keypose = openpose_keypose.to(opt.device)
    elif cond_inp_type == 'image':
        with autocast('cuda', dtype=torch.float32):
            openpose_keypose = cond_model(openpose_keypose)
        openpose_keypose = img2tensor(openpose_keypose).unsqueeze(0) / 255.
        openpose_keypose = openpose_keypose.to(opt.device)

    else:
        raise NotImplementedError

    return openpose_keypose


def get_adapter_feature(inputs, adapters):
    ret_feat_map = None
    ret_feat_seq = None
    if not isinstance(inputs, list):
        inputs = [inputs]
        adapters = [adapters]

    for input, adapter in zip(inputs, adapters):
        cur_feature = adapter['model'](input)
        if isinstance(cur_feature, list):
            if ret_feat_map is None:
                ret_feat_map = list(map(lambda x: x * adapter['cond_weight'], cur_feature))
            else:
                ret_feat_map = list(map(lambda x, y: x + y * adapter['cond_weight'], ret_feat_map, cur_feature))
        else:
            if ret_feat_seq is None:
                ret_feat_seq = cur_feature * adapter['cond_weight']
            else:
                ret_feat_seq = torch.cat([ret_feat_seq, cur_feature * adapter['cond_weight']], dim=1)

    return ret_feat_map, ret_feat_seq
