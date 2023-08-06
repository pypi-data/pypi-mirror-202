import torch
from torchvision import transforms
from torchvision import models
from torchvision.models import *
from torch.utils.data import Dataset, DataLoader
from PIL import Image
from tqdm import tqdm
import os


class ImgDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.file = os.listdir(root_dir)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.file)

    def __getitem__(self, index):
        img_name = os.path.join(self.root_dir, self.file[index])
        image = Image.open(img_name).convert('RGB')
        image = self.transform(image)
        label = self.file[index]
        return image, label


class Img2Vec:
    def __init__(self, model_name: str = 'resnet18'):
        self.device = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Using {self.device} device")
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.model_weights = {
            "resnet18": ResNet18_Weights.DEFAULT,
            "resnet34": ResNet34_Weights.DEFAULT,
            "resnet50": ResNet50_Weights.DEFAULT,
            "resnet101": ResNet101_Weights.DEFAULT,
            "resnet152": ResNet152_Weights.DEFAULT,
            "alexnet": AlexNet_Weights.DEFAULT,
        }
        self.model_name = model_name
        if self.model_name in ["resnet18", "resnet34", "resnet50", "resnet101", "resnet152", "alexnet"]:
            self.model = getattr(models, self.model_name)(weights=self.model_weights[self.model_name]).to(
                self.device).eval()
            print(self.model_name, "model loaded")
        else:
            raise ValueError("Invalid model name")

    def get_vec(self, filepath: str) -> list:
        """获取单一图片向量

        :param filepath:图片路径
        :return:
        """
        input_image = Image.open(filepath).convert('RGB')
        input_tensor = self.preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0).to(self.device)
        output = self.model(input_batch)
        filename = os.path.basename(filepath)
        return [(filename, output.detach().cpu().numpy().tolist()[0])]

    def get_list_vec(self, root_dir: str, batch_size: int = 32) -> list:
        """获取文件夹下所有图片向量

        :param root_dir: 图片文件夹路径
        :param batch_size:  批处理大小
        :return:
        """
        img_dataset = ImgDataset(root_dir=root_dir, transform=self.preprocess)
        img_loader = DataLoader(img_dataset, batch_size=batch_size, shuffle=True)
        results = []
        for x, y in tqdm(img_loader):
            x = x.to(self.device)
            with torch.no_grad():
                output = self.model(x)
            for i in range(len(output)):
                results.append((y[i], output[i].detach().cpu().numpy().tolist()))
        return results
