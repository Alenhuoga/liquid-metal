from predict_project.LSTMModel import lstm

from predict_project.dataset import getData,getDataDensity,getDataSolidity,getDataViscosity,getData_heat_conductivity,getDataConductivity
from predict_project.parser_my import args
import torch
import os
import numpy as np

#密度预测函数
def predict_density(Mg=0,Al=0,Fe=0,Co=0,Ni=0,Cu=0,Zn=4,Ga=67,Ag=0,In=29,Sn=0,Bi=0,model_name=args.save_file_density):
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    # 加载模型 进行预测
    checkpoint = torch.load(model_name)

    model.load_state_dict(checkpoint['state_dict'])
    list_x=[]

    list_x.append(Mg)
    list_x.append(Al)
    list_x.append(Fe)
    list_x.append(Co)
    list_x.append(Ni)
    list_x.append(Cu)
    list_x.append(Zn)
    list_x.append(Ga)
    list_x.append(Ag)
    list_x.append(In)
    list_x.append(Sn)
    list_x.append(Bi)
    print(type(list_x))
    print(list_x)


    list_x = torch.tensor(list_x)
    list_x = list_x.unsqueeze(0).unsqueeze(0)


    list_x = list_x.float()
    print(list_x.size())
    print(list_x.type())


    print(list_x)
    pred = model(list_x)

    #转为列表
    pred = pred.tolist()
    print(pred)
    #降维
    pred = str(pred)
    pred = pred.replace('[','')
    pred = pred.replace(']','')
    pred = list(eval(pred))
    print('降维后的数据为：'+str(pred))
    print('密度预测为：' + str(pred[1]))
    # print('预测结果为：'+str(pred.item()))
    return float(str(pred[1]))

#热导率预测函数
def predict_heat_conductivity(Mg=0,Al=0,Fe=0,Co=0,Ni=0,Cu=0,Zn=4,Ga=67,Ag=0,In=29,Sn=0,Bi=0,model_name=args.save_file_heat_conductivity):
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    # 加载模型 进行预测
    checkpoint = torch.load(model_name)

    model.load_state_dict(checkpoint['state_dict'])
    list_x=[]

    list_x.append(Mg)
    list_x.append(Al)
    list_x.append(Fe)
    list_x.append(Co)
    list_x.append(Ni)
    list_x.append(Cu)
    list_x.append(Zn)
    list_x.append(Ga)
    list_x.append(Ag)
    list_x.append(In)
    list_x.append(Sn)
    list_x.append(Bi)
    print(type(list_x))
    print(list_x)


    list_x = torch.tensor(list_x)
    list_x = list_x.unsqueeze(0).unsqueeze(0)


    list_x = list_x.float()
    print(list_x.size())
    print(list_x.type())


    print(list_x)
    pred = model(list_x)

    #转为列表
    pred = pred.tolist()
    print(pred)
    #降维
    pred = str(pred)
    pred = pred.replace('[','')
    pred = pred.replace(']','')
    pred = list(eval(pred))
    print('降维后的数据为：'+str(pred))
    print('热导率预测为：' + str(pred[1]))
    return float(str(pred[1]))
    # print('预测结果为：'+str(pred.item()))

#导电率预测函数
def predict_conductivity(Mg=0,Al=0,Fe=0,Co=0,Ni=0,Cu=0,Zn=4,Ga=67,Ag=0,In=29,Sn=0,Bi=0,model_name=args.save_file_conductivity):
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    # 加载模型 进行预测
    checkpoint = torch.load(model_name) #修改模型在这里

    model.load_state_dict(checkpoint['state_dict'])
    list_x=[]

    list_x.append(Mg)
    list_x.append(Al)
    list_x.append(Fe)
    list_x.append(Co)
    list_x.append(Ni)
    list_x.append(Cu)
    list_x.append(Zn)
    list_x.append(Ga)
    list_x.append(Ag)
    list_x.append(In)
    list_x.append(Sn)
    list_x.append(Bi)
    print(type(list_x))
    print(list_x)


    list_x = torch.tensor(list_x)
    list_x = list_x.unsqueeze(0).unsqueeze(0)


    list_x = list_x.float()
    print(list_x.size())
    print(list_x.type())


    print(list_x)
    pred = model(list_x)

    #转为列表
    pred = pred.tolist()
    print(pred)
    #降维
    pred = str(pred)
    pred = pred.replace('[','')
    pred = pred.replace(']','')
    pred = list(eval(pred))
    print('降维后的数据为：'+str(pred))
    print('电导率预测为：' + str(pred[1]))
    return float(str(pred[1]))
    # print('预测结果为：'+str(pred.item()))

#硬度预测函数
def predict_solidity(Mg=0,Al=0,Fe=0,Co=0,Ni=0,Cu=0,Zn=4,Ga=67,Ag=0,In=29,Sn=0,Bi=0,model_name=args.save_file_solidity):
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    # 加载模型 进行预测
    checkpoint = torch.load(model_name) #修改模型在这里

    model.load_state_dict(checkpoint['state_dict'])
    list_x=[]

    list_x.append(Mg)
    list_x.append(Al)
    list_x.append(Fe)
    list_x.append(Co)
    list_x.append(Ni)
    list_x.append(Cu)
    list_x.append(Zn)
    list_x.append(Ga)
    list_x.append(Ag)
    list_x.append(In)
    list_x.append(Sn)
    list_x.append(Bi)
    print(type(list_x))
    print(list_x)


    list_x = torch.tensor(list_x)
    list_x = list_x.unsqueeze(0).unsqueeze(0)


    list_x = list_x.float()
    print(list_x.size())
    print(list_x.type())


    print(list_x)
    pred = model(list_x)

    #转为列表
    pred = pred.tolist()
    print(pred)
    #降维
    pred = str(pred)
    pred = pred.replace('[','')
    pred = pred.replace(']','')
    pred = list(eval(pred))
    print('降维后的数据为：'+str(pred))
    print('硬度预测为：' + str(pred[1]))
    return float(str(pred[1]))
    # print('预测结果为：'+str(pred.item()))

#粘度预测函数
def predict_viscosity(Mg=0,Al=0,Fe=0,Co=0,Ni=0,Cu=0,Zn=4,Ga=67,Ag=0,In=29,Sn=0,Bi=0,model_name=args.save_file_viscosity):
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    # 加载模型 进行预测
    checkpoint = torch.load(model_name) #修改模型在这里

    model.load_state_dict(checkpoint['state_dict'])
    list_x=[]

    list_x.append(Mg)
    list_x.append(Al)
    list_x.append(Fe)
    list_x.append(Co)
    list_x.append(Ni)
    list_x.append(Cu)
    list_x.append(Zn)
    list_x.append(Ga)
    list_x.append(Ag)
    list_x.append(In)
    list_x.append(Sn)
    list_x.append(Bi)
    print(type(list_x))
    print(list_x)


    list_x = torch.tensor(list_x)
    list_x = list_x.unsqueeze(0).unsqueeze(0)


    list_x = list_x.float()
    print(list_x.size())
    print(list_x.type())


    print(list_x)
    pred = model(list_x)

    #转为列表
    pred = pred.tolist()
    print(pred)
    #降维
    pred = str(pred)
    pred = pred.replace('[','')
    pred = pred.replace(']','')
    pred = list(eval(pred))
    print('降维后的数据为：'+str(pred))
    print('粘度预测为：' + str(pred[1]))
    return float(str(pred[1]))
    # print('预测结果为：'+str(pred.item()))


# predict_density()
# predict_density(0,0,0,0,0,0,0,0,0,0,42,58)
#
# predict_heat_conductivity()
#
# predict_conductivity()
#
# predict_viscosity()
#
# predict_solidity()