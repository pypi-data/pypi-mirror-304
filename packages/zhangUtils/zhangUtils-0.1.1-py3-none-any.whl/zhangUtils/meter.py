__version__ = '0.1.1'


from skimage import io
from torchvision import transforms
from skimage.metrics import structural_similarity, peak_signal_noise_ratio
import torch
import torch.nn.functional as F

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