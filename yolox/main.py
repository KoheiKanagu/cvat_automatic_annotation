import base64
import json

import cv2
import numpy as np
import torch
import yaml

from yolox.data.data_augment import ValTransform
from yolox.exp import get_exp
from yolox.utils import postprocess

# Reference:
# https://github.com/Megvii-BaseDetection/YOLOX/blob/0.2.0/tools/demo.py#L17
# https://github.com/openvinotoolkit/cvat/blob/v2.0.0/serverless/openvino/omz/public/yolo-v3-tf/nuclio/main.py


def init_context(context):
    with open("/opt/nuclio/function.yaml", 'rb') as function_file:
        functionconfig = yaml.safe_load(function_file)

    labels_spec = functionconfig['metadata']['annotations']['spec']
    labels = {item['id']: item['name'] for item in json.loads(labels_spec)}
    context.user_data.labels = labels

    exp = get_exp("/opt/nuclio/yolox_tiny.py")
    exp.num_classes = len(labels)
    context.user_data.exp = exp

    model = exp.get_model()
    model.eval()

    ckpt_file = "/opt/nuclio/best_ckpt.pth"
    ckpt = torch.load(ckpt_file, map_location="cpu")

    model.load_state_dict(ckpt["model"])
    context.user_data.model = model


def handler(context, event):
    model = context.user_data.model
    exp = context.user_data.exp
    labels = context.user_data.labels
    test_size = exp.input_scale
    num_classes = exp.num_classes
    confthre = exp.test_conf
    nmsthre = exp.nmsthre

    data = event.body
    threshold = float(data.get("threshold", 0.5))

    img_binary = base64.b64decode(data["image"])
    jpg = np.frombuffer(img_binary, dtype=np.uint8)
    img = cv2.imdecode(jpg, cv2.IMREAD_COLOR)

    ratio = min(test_size[0] / img.shape[0], test_size[1] / img.shape[1])
    preproc = ValTransform()

    img, _ = preproc(img, None, test_size)
    img = torch.from_numpy(img).unsqueeze(0)
    img = img.float()

    with torch.no_grad():
        outputs = model(img)

        outputs = postprocess(
            outputs,
            num_classes,
            confthre,
            nmsthre,
            class_agnostic=True
        )

    results = []

    for output in outputs:
        if output is None:
            continue
        bboxes = output[:, 0:4]
        bboxes /= ratio

        cls = output[:, 6]
        scores = output[:, 4] * output[:, 5]

        for i, score in enumerate(scores):
            if score >= threshold:
                results.append({
                    "confidence": score.tolist(),
                    "label": labels.get(cls[i].tolist()+1, "unknown"),
                    "points": bboxes[i].tolist(),
                    "type": "rectangle",
                })

    return context.Response(
        body=json.dumps(results),
        headers={},
        content_type='application/json',
        status_code=200
    )
