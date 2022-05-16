import argparse
import torch
import os

abpath = os.path.abspath('.')+'/predict_project'
print(abpath)
parser = argparse.ArgumentParser()



parser.add_argument('--corpusFile', default=abpath+'/data/000001SH_index.csv')
parser.add_argument('--metalFile', default=abpath +'/data/total.csv')

# TODO 常改动参数
parser.add_argument('--gpu', default=1, type=int) # gpu 卡号
parser.add_argument('--epochs', default=100, type=int) # 训练轮数
parser.add_argument('--layers', default=2, type=int) # LSTM层数
parser.add_argument('--input_size', default=8, type=int) #输入特征的维度

parser.add_argument('--input_size1', default=21, type=int) #液态金属输入特征的维度

parser.add_argument('--hidden_size', default=32, type=int) #隐藏层的维度
parser.add_argument('--lr', default=0.0001, type=float) #learning rate 学习率
parser.add_argument('--sequence_length', default=5, type=int) # sequence的长度，默认是用前五天的数据来预测下一天的收盘价
parser.add_argument('--batch_size', default=64, type=int)
parser.add_argument('--useGPU', default=False, type=bool) #是否使用GPU
parser.add_argument('--batch_first', default=True, type=bool) #是否将batch_size放在第一维
parser.add_argument('--dropout', default=0.1, type=float)
parser.add_argument('--save_file', default=abpath + '/model/stock.pkl') # 模型保存位置



parser.add_argument('--save_file_density', default=abpath + '/model/metal_density.pkl') # 密度模型保存位置
parser.add_argument('--save_file_heat_conductivity', default=abpath + '/model/metal_heat_conductivity.pkl') # 热导率模型保存位置
parser.add_argument('--save_file_conductivity', default=abpath + '/model/metal_conductivity.pkl') # 导电率模型保存位置
parser.add_argument('--save_file_solidity', default=abpath + '/model/metal_solidity.pkl') # 硬度模型保存位置
parser.add_argument('--save_file_viscosity', default=abpath + '/model/metal_viscosity.pkl') # 粘度模型保存位置


args = parser.parse_args(args=[])

device = torch.device(f"cuda:{args.gpu}" if torch.cuda.is_available() and args.useGPU else "cpu")
args.device = device