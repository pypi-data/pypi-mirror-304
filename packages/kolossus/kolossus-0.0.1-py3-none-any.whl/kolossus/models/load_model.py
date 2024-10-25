
import torch
from .Network import Network

# note: very hacky, change to host on some website in the future 
import os
import sys 

if not os.path.isfile(os.path.join(os.path.split(__file__)[0], 'saved_model_cs_ws_ft_v3_humansty.pth')):
    print("Error: please save file saved_model_cs_ws_ft_v3_humansty.pth to", os.path.split(__file__)[0], 
          "sorry, very bad programming practice, will be fixed later", file=sys.stderr)
    sys.exit(1)


def load_model():
    path = os.path.split(__file__)[0]
    model_weights = os.path.join(path, 'new_ft_v3_humansty.pth')
    model = Network()
    model.load_state_dict(torch.load(model_weights))
    return model 
