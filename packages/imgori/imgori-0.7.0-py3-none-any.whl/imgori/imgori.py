import functools

import torch
from torch import nn
from torchvision.transforms._presets import ImageClassification

from .models import DEFAULT_MODEL
from .nn import mobilenet_v3
from .types import Orientation
from .types import PILImage
from .utils import download_url
from .utils import timeit


@functools.cache
def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


@functools.cache
def get_model(model_path: str | None = None) -> nn.Module:
    device = get_device()

    if model_path is None:
        model_path = DEFAULT_MODEL

    if model_path.startswith(("s3://", "http://", "https://")):
        model_path = download_url(model_path)

    state_dict = torch.load(model_path, map_location=device, weights_only=True)

    model = mobilenet_v3(num_classes=len(Orientation))
    model.load_state_dict(state_dict["model"])
    model.eval()
    return model.to(device)


@functools.cache
def get_transform() -> ImageClassification:
    return ImageClassification(crop_size=224, resize_size=256)


@torch.no_grad()
def predict(img: PILImage) -> Orientation:
    device = get_device()
    model = get_model()
    transform = get_transform()

    img_tensor = transform(img)
    img_tensor = img_tensor.unsqueeze(0).to(device)
    output = model(img_tensor)
    output = output.argmax(dim=1).item()
    return Orientation(output)


class Imgori:
    model: nn.Module
    transform: ImageClassification

    def __init__(
        self,
        model_path: str | None = None,
        device: torch.device | str = "cpu",
    ):
        self.device = device
        self.transform = ImageClassification(crop_size=224, resize_size=256)

        self.model = self.load_model(model_path or DEFAULT_MODEL)

    def load_model(self, model_path: str) -> nn.Module:
        if model_path.startswith(("s3://", "http://", "https://")):
            model_path = download_url(model_path)

        state_dict = torch.load(model_path, map_location=self.device, weights_only=True)

        model = mobilenet_v3(num_classes=len(Orientation))
        model.load_state_dict(state_dict["model"])
        model.eval()
        return model.to(self.device)

    @timeit
    @torch.no_grad()
    def __call__(self, img: PILImage) -> Orientation:
        img_tensor = self.transform(img)
        img_tensor = img_tensor.unsqueeze(0).to(self.device)
        output = self.model(img_tensor)
        output = output.argmax(dim=1).item()
        return Orientation(output)
