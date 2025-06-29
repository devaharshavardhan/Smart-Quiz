import random
import torch
import time
def set_seed():
    seed = int(time.time() * 1000) % 100000
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
