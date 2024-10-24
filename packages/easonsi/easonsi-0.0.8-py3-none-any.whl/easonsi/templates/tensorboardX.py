# -*- coding: utf-8 -*-
# @Author  : Miaoshuyu
# @Email   : miaohsuyu319@163.com
import torch
import torchvision.utils as vutils
import numpy as np
import torchvision.models as models
from torchvision import datasets
from tensorboardX import SummaryWriter

""" 
from https://github.com/miaoshuyu/pytorch-tensorboardx-visualization
"""

resnet18 = models.resnet18(False)

# 1) 初始化 writer
# 不指定 logdir 默认保存到 runs/May04_22-14-54_s-MacBook-Pro.local, comment 加上后缀
writer = SummaryWriter(comment="_demo")
sample_rate = 44100
freqs = [262, 294, 330, 349, 392, 440, 440, 440, 440, 440, 440]

for n_iter in range(100):
    dummy_s1 = torch.rand(1)
    dummy_s2 = torch.rand(1)
    
    # 2.1) 写入 scalar
    # data grouping by `slash`
    writer.add_scalar('data/scalar1', dummy_s1[0], n_iter)
    writer.add_scalar('data/scalar2', dummy_s2[0], n_iter)
    # 记录一组数字, 画在一张图上
    writer.add_scalars('data/scalar_group', {'xsinx': n_iter * np.sin(n_iter),
                                             'xcosx': n_iter * np.cos(n_iter),
                                             'arctanx': np.arctan(n_iter)}, n_iter)

    # 下面的 image, audio, text, histogram 每10轮写一次
    if n_iter % 10 == 0:
        # 2.2) 写入 images
        dummy_img = torch.rand(32, 3, 64, 64)  # output from network
        x = vutils.make_grid(dummy_img, normalize=True, scale_each=True)
        writer.add_image('Image', x, n_iter)

        # 2.3) 写入 audio
        dummy_audio = torch.zeros(sample_rate * 2)
        for i in range(x.size(0)):
            # amplitude of sound should in [-1, 1]
            dummy_audio[i] = np.cos(freqs[n_iter // 10] * np.pi * float(i) / float(sample_rate))
        writer.add_audio('myAudio', dummy_audio, n_iter, sample_rate=sample_rate)

        # 2.4) 写入 text
        writer.add_text('Text', 'text logged at step:' + str(n_iter), n_iter)

        # 2.5) 写入 histogram, 查看参数分布情况
        for name, param in resnet18.named_parameters():
            writer.add_histogram(name, param.clone().cpu().data.numpy(), n_iter)

        # 2.6) 写入 Precision-Recall Curve
        # needs tensorboard 0.4RC or later
        writer.add_pr_curve('xoxo', np.random.randint(2, size=100), np.random.rand(100), n_iter)

# 3) 添加 Graph
sample_input = torch.tensor(np.random.random(size=(5,3, 224,224)), dtype=torch.float32)
writer.add_graph(resnet18, (sample_input,))

# 4) 添加 embedding (在Tensorboard中选择「Projector」)
dataset = datasets.MNIST('mnist', train=False, download=True)
images = dataset.test_data[:100].float() # [100, 28, 28]
label = dataset.test_labels[:100]
features = images.view(100, 784) # 展开成一维直接作为 784 维的 feature
writer.add_embedding(features, metadata=label, label_img=images.unsqueeze(1)) # [100, 1, 28, 28]

# 5) 将所有的 scaler 抽取出来 (例如这里保存的是 add_scalars 所记录的)
# {writer_id : [[timestamp, step, value], ...], ...}
# export scalar data to JSON for external processing
writer.export_scalars_to_json("./all_scalars.json")
writer.close()