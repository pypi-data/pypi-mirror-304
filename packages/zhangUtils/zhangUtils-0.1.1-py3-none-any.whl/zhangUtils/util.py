__version__ = '0.1.1'

"""
实现你自己的轮子的功能
"""

import torchvision
from torchvision import transforms
import torch
import numpy as np
from PIL import Image
from skimage import io
from skimage.metrics import structural_similarity, peak_signal_noise_ratio
import torch.nn.functional as F

def show(img):

    if torch.is_tensor(img) | isinstance(img, np.ndarray):
        img = transforms.ToPILImage()(img)
    
    img.show()

def shape(tensor):
    print(tensor.size())

def save_image(img, img_path='./images/'):
    if isinstance(img, np.ndarray):
        img = torch.from_numpy(img)
    
    if torch.is_tensor(img):
        torchvision.utils.save_image(img, img_path)
        return

    img.save(img_path)



def ssim(cleanImagePath, dehazeImagePath):
    clean_image = transforms.ToTensor()(io.imread(cleanImagePath))
    dehaze_image = transforms.ToTensor()(io.imread(dehazeImagePath))
    ssim_val = structural_similarity(clean_image.permute(1, 2, 0).cpu().numpy(), 
                                     dehaze_image.permute(1, 2, 0).numpy(), data_range=1, multichannel=True)
    return ssim_val

def psnr(cleanImagePath, dehazeImagePath):
    clean_image = transforms.ToTensor()(io.imread(cleanImagePath))
    dehaze_image = transforms.ToTensor()(io.imread(dehazeImagePath))
    psnr_val = 10 * torch.log10(1 / F.mse_loss(dehaze_image, clean_image))
    return psnr_val.item()
    



  