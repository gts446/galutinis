import ESRGAN.RRDBNet_arch as arch
import ARCNN.model as arcnn
import torch
import torchvision.transforms as transforms
from PIL import Image

def upscale_image(image:Image):

    model_path = 'ESRGAN/models/RRDB_ESRGAN_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
    # device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu

    model = arch.RRDBNet(3, 3, 64, 23)

    model.load_state_dict(torch.load(model_path, weights_only=True), strict=True)
    model.eval()  

    transform = transforms.ToTensor()
    image_tensor = transform(image.convert('RGB'))
    with torch.no_grad():
        output:torch.Tensor = model(image_tensor.unsqueeze(0))
    
    output = output.squeeze(0).clamp(0, 1).numpy() * 255
    image = Image.fromarray(output.transpose(1,2,0).astype('uint8'), mode='RGB')

    return image

def filter_artifacts(image:Image):

    model = arcnn.ARCNN()

    model.load_state_dict(torch.load('arcnn_parameters.pth', weights_only=True), strict=True)
    model.eval()  

    transform = transforms.ToTensor()
    image_tensor = transform(image.convert('RGB'))
    with torch.no_grad():
        output:torch.Tensor = model(image_tensor.unsqueeze(0))
    
    output = output.squeeze(0).clamp(0, 1).numpy() * 255
    image = Image.fromarray(output.transpose(1,2,0).astype('uint8'), mode='RGB')

    return image