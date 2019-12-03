''' File with the logic and math to calculate a prediction and get the heatmap. '''

import io
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2
import matplotlib.cm as cm
import base64

from .model import create_load_model


model = None
preprocess = None
features = None
device = None
pixel_intensity = 0.6
downscale = 0.3


class saveFeatures():
    ''' Class to put a hook up on the model so we
        can get the features for the heatmaps. '''
    features=None
    def __init__(self, m):
        self.hook = m.register_forward_hook(self.hook_fn)

    def hook_fn(self, module, input, output):
        self.features = ((output.cpu()).data).numpy()

    def remove(self):
        self.hook.remove()


def load_model():
    global model, preprocess, features, device

    # Set up the model
    model, feature_layer, device = create_load_model()

    # Transforms
    preprocess = transforms.Compose([  # Transformations applied to all images
            transforms.Resize([224]*2, Image.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize([0.0466, 0.1761, 0.3975], [
                                 0.8603, 0.8790, 0.8751])
        ])

    # Hook up for heatmaps
    features = saveFeatures(feature_layer)


def getCAM(feature_conv, weight_fc, discard):
    _, nc, h, w = feature_conv.shape
    cam = weight_fc[discard].dot(feature_conv.reshape((nc, h*w)))
    cam = cam.reshape(h, w)
    cam = cam - np.min(cam)
    cam_img = cam / np.max(cam)
    cam_img = cm.jet_r(cam_img)[..., :3] * 255.0
    cam_img *= pixel_intensity
    return cam_img


def predict_image(image):
    image = Image.open(io.BytesIO(image))
    image = image.convert('RGB')

    # Preprocess the image and prepare it for classification
    input_image = preprocess(image).unsqueeze(0).to(device)

    outputs = model(input_image)

    _, preds = torch.max(outputs, 1)

    fc_params = list(model._modules.get('fc').parameters())
    fc = np.squeeze(fc_params[0].data.numpy())
    heatmap = getCAM(features.features, fc, preds)

    width, height = image.size
    width, height = int(width*downscale), int(height*downscale)
    image = np.array(image, dtype=float)
    image = cv2.resize(image, (width, height))
    heatmap = cv2.resize(heatmap, (width, height))
    heatmap = (heatmap.astype(np.float) + image) / 2

    pil_img = Image.fromarray(heatmap.astype('uint8'))
    buff = io.BytesIO()
    pil_img.save(buff, format="PNG")
    heatmap = base64.b64encode(buff.getvalue()).decode("utf-8")

    pil_img = Image.fromarray(image.astype('uint8'))
    buff2 = io.BytesIO()
    pil_img.save(buff2, format="PNG")
    image = base64.b64encode(buff2.getvalue()).decode("utf-8")

    return F.softmax(outputs, dim=1).tolist()[0], image, heatmap
