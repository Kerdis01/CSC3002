from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
# from torchvision.models.detection import ssd300_vgg16, SSD300_VGG16_Weights

def get_model(device):
    # load the model 
    # model = ssd300_vgg16(weights=SSD300_VGG16_Weights.DEFAULT)
    model = ssdlite320_mobilenet_v3_large(weights=SSDLite320_MobileNet_V3_Large_Weights.DEFAULT)
    # load the model onto the computation device
    model = model.eval().to(device)
    return model