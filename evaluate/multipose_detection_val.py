import os, sys
root_path = os.path.realpath(__file__).split('/evaluate/multipose_detection_val.py')[0]
os.chdir(root_path)
sys.path.append(root_path)

from torch.utils.data import DataLoader
from torchvision import transforms

from training.batch_processor import batch_processor
from datasets.coco_data.RetinaNet_data_pipeline import (AspectRatioBasedSampler,
                                                        CocoDataset,
                                                        Normalizer, Resizer,
                                                        collater)
from network.posenet import poseNet
from evaluate.tester import Tester

# Hyper-params
coco_root = '/data/COCO/'
backbone = 'resnet101'  # 'resnet50'

# Set Training parameters
params = Tester.TestParams()
params.subnet_name = 'detection_subnet'
params.gpus = [0]
params.ckpt = './demo/models/ckpt_baseline_resnet101.h5'
params.batch_size = 1 * len(params.gpus)
params.print_freq = 100

# validation data
dataset_val = CocoDataset(coco_root, set_name='val2017',
                          transform=transforms.Compose([Normalizer(), Resizer()]))
sampler_val = AspectRatioBasedSampler(
    dataset_val, batch_size=params.batch_size, drop_last=False)
valid_data = DataLoader(dataset_val, num_workers=3,
                        collate_fn=collater, batch_sampler=sampler_val)
print('val dataset len: {}'.format(len(valid_data.dataset)))

# model
if backbone == 'resnet101':
    model = poseNet(101)
elif backbone == 'resnet50':
    model = poseNet(50)


tester = Tester(model, params, batch_processor, valid_data)
tester.val()
