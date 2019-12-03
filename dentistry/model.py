''' File to create and load the model, or update the model
    weights in case that there is an update. '''

import torch
import torch.nn as nn
from torchvision import models

def create_load_model():
    ''' Returns the loaded model ready to predict '''
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 2)

    # cuda = torch.cuda.is_available()

    # if cuda:
        # model.load_state_dict(torch.load('model/dentistry_weights.pth'))
    # else:
    model.load_state_dict(torch.load('dentistry_weights.pth', map_location=lambda storage, loc: storage))

    device = torch.device("cpu")# "cuda" if cuda else "cpu")
    model = model.to(device)
    model.eval()

    feature_layer = list(model.children())[-3]

    return model, feature_layer, device

def update_model_weights():
    ''' Method for later download new model weights from the web. '''
    pass
