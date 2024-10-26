#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import numpy as np
import h5py
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from vit_mlp_7 import *  # 确保这个导入是正确的
import logging

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='training_log.log',
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)



SEED = 1254
torch.manual_seed(SEED)
np.random.seed(SEED)
## case2
NUM_SUBCARRIERS = 96
NUM_OFDM_SYMBOLS = 12
NUM_LAYERS = 4
NUM_BITS_PER_SYMBOL = 6
WEIGHT_DECAY = 1e-4
EPOCHS = 20000
BATCH_SIZE = 40
LEARNING_RATE = 0.0012
STEP_SIZE = 10000  # 每50个epoch减少学习率
GAMMA = 0.7  # 学习率减少的倍数

train_dataset_dir = './../data/'  # 根据你的数据路径进行设置

# 数据加载
logging.info('=====================load case1 data===============')
f = h5py.File(os.path.join(train_dataset_dir, "D2.hdf5"), 'r')
rx_signal = f['rx_signal'][:]
tx_bits = f['tx_bits'][:]
pilot = f['pilot'][:]
f.close()
pilot_O=pilot.copy()
pilot_O = torch.from_numpy(pilot_O).float() 

samples = rx_signal.shape[0]
pilot = np.tile(pilot, (samples, 1, 1, 1, 1))

# 数据集分割
split_idx = int(rx_signal.shape[0] * 0.99)
rx_signal_train, rx_signal_val = rx_signal[:split_idx], rx_signal[split_idx:]
pilot_train, pilot_val = pilot[:split_idx], pilot[split_idx:]
tx_bits_train, tx_bits_val = tx_bits[:split_idx], tx_bits[split_idx:]


# 转换为PyTorch张量并创建数据加载器
train_dataset = TensorDataset(torch.from_numpy(rx_signal_train).float(),
                              torch.from_numpy(pilot_train).float(),
                              torch.from_numpy(tx_bits_train).float())
val_dataset = TensorDataset(torch.from_numpy(rx_signal_val).float(),
                            torch.from_numpy(pilot_val).float(),
                            torch.from_numpy(tx_bits_val).float())

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

'''
model = Neural_receiver(subcarriers = 96,
                        num_symbols = 12, 
                        streams = 4,
                        num_bits_per_symbol = 6,
                        num_patches = 1152,
                        num_layers=6, hidden_dim=384, tokens_mlp_dim=512, channels_mlp_dim=2048, 
                        num_blocks=4, base_channels=512,                       
                        ).cuda()
'''
model = Neural_receiver(num_symbols=12, num_heads=8, subcarriers=96, streams=4,
                            num_layers=7, hidden_dim=512, ffn_hidden=2048, num_bits_per_symbol=6, dropout_rate=0.03).cuda()
#model.apply(init_weights)

criterion = nn.BCEWithLogitsLoss().cuda()

optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
#optimizer = optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHReluT_DECAY)


scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=STEP_SIZE, gamma=GAMMA)  # 学习率调度器
#scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=20, eta_min=1e-7)  # 使用余弦退火策略
# 模型训练和保存
best_loss = float('inf')
for epoch in range(EPOCHS):
    model.train()
    total_loss, total_acc = 0, 0
    for rx_signal_batch, pilot_batch, tx_bits_batch in train_loader:
        rx_signal_batch, pilot_batch, tx_bits_batch = rx_signal_batch.cuda(), pilot_batch.cuda(), tx_bits_batch.cuda()
        optimizer.zero_grad()
        output = model(rx_signal_batch, pilot_batch)
        loss = criterion(output, tx_bits_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        # 改进的准确率计算
        predicted = torch.sigmoid(output) >= 0.5
        total_acc += (predicted.float() == tx_bits_batch).float().mean().item()
    scheduler.step()  # 更新学习率

    # 验证
    model.eval()
    total_val_loss, total_val_acc = 0, 0
    with torch.no_grad():
        for rx_signal_batch, pilot_batch, tx_bits_batch in val_loader:
            rx_signal_batch, pilot_batch, tx_bits_batch = rx_signal_batch.cuda(), pilot_batch.cuda(), tx_bits_batch.cuda()
            output = model(rx_signal_batch, pilot_batch)
            val_loss = criterion(output, tx_bits_batch)
            total_val_loss += val_loss.item()
            predicted = torch.sigmoid(output) >= 0.5
            total_val_acc += (predicted.float() == tx_bits_batch).float().mean().item()

    # 打印指标
    logging.info(f'Epoch {epoch}: Train Loss {total_loss / len(train_loader):.4f}, '
                 f'Train Acc {total_acc / len(train_loader):.4f}, '
                 f'Val Loss {total_val_loss / len(val_loader):.4f}, '
                 f'Val Acc {total_val_acc / len(val_loader):.4f}')

    # 保存最佳模型
    if total_val_loss / len(val_loader) < best_loss:
        best_loss = total_val_loss / len(val_loader)
        torch.save(model, 'receiver_2.pth.tar')  
        logging.info("Model saved")

torch.cuda.empty_cache()  # 训练结束后清理内存
logging.info('Training for case_1a is finished!')


# In[ ]:




