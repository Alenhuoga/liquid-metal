from torch.autograd import Variable
import torch.nn as nn
import torch
from predict_project.LSTMModel import lstm
from predict_project.parser_my import args
from predict_project.dataset import getData,getDataDensity,getDataSolidity,getDataViscosity,getData_heat_conductivity,getDataConductivity
import matplotlib.pyplot as plt
from visdom import Visdom

def train():

    #训练结果可视化
    viz = Visdom()
    viz.line([0.], [0.], win='train_loss', opts=dict(title='train loss'))

    model = lstm(input_size=args.input_size, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    model.to(args.device)
    criterion = nn.MSELoss()  # 定义损失函数
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # Adam梯度下降  学习率=0.001

    close_max, close_min, train_loader, test_loader = getData(args.corpusFile,args.sequence_length,args.batch_size )
    for i in range(args.epochs):
        total_loss = 0
        for idx, (data, label) in enumerate( ):
            if args.useGPU:
                data1 = data.squeeze(1).cuda()
                pred = model(Variable(data1).cuda())
                # print(pred.shape)
                pred = pred[1,:,:]
                label = label.unsqueeze(1).cuda()
                # print(label.shape)
            else:
                data1 = data.squeeze(1)
                # print(data1.shape)

                #带入模型得出当前预测值
                pred = model(Variable(data1))
                pred = pred[1, :, :]
                label = label.unsqueeze(1)

            #目标优化函数 label是真实y pred是预测的y
            loss = criterion(pred, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()


        viz.line([loss.item()],[i],win='train_loss',update='append')

        #打印当前损失
        log = '当前损失为'+str(total_loss)
        print(log)
        if i % 10 == 0:
            # torch.save(model, args.save_file)
            torch.save({'state_dict': model.state_dict()}, args.save_file)
            print('第%d epoch，保存模型' % i)
    # torch.save(model, args.save_file)
    torch.save({'state_dict': model.state_dict()}, args.save_file)

#训练密度网络
def trainDensity():

    viz = Visdom()
    viz.line([0.], [0.], win='train_loss_d', opts=dict(title='train loss d'))
    print('开始训练密度网络')

    #更改输入的size 根据自己的数据
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    model.to(args.device)
    criterion = nn.MSELoss()  # 定义损失函数
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # Adam梯度下降  学习率=0.001


    #加载密度数据
    train_loader, test_loader ,data_num= getDataDensity(args.metalFile,args.sequence_length,args.batch_size)
    for i in range(10000):
        total_loss = 0
        for idx, (data, label) in enumerate(train_loader):
            if args.useGPU:
                print('使用gpu进行运算')
                data1 = data.cuda()
                pred = model(Variable(data1).cuda())
                # print(pred.shape)
                pred = pred[1,:,:]
                label = label.unsqueeze(1).cuda()
                # print(label.shape)
            else:

                # data1 = data.squeeze(1)
                data1 = data

                #带入模型得出当前预测值
                pred = model(Variable(data1))
                pred = pred[1, :, :]
                label = label.unsqueeze(1)

            #目标优化函数 label是真实y pred是预测的y
            loss = criterion(pred, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()


        viz.line([total_loss], [i], win='train_loss_d', update='append')
        log = '当前损失为' + str(total_loss)
        print(log)
        if i % 10 == 0:
            # torch.save(model, args.save_file)
            torch.save({'state_dict': model.state_dict()}, args.save_file_density)
            print('第%d epoch，保存模型' % i)
    # torch.save(model, args.save_file)
    torch.save({'state_dict': model.state_dict()}, args.save_file_density)

#训练热导率网络
def train_heat_conductivity():
    viz = Visdom()
    viz.line([0.], [0.], win='train_loss_h', opts=dict(title='train loss h'))

    print('开始训练热导率网络')

    #更改输入的size 根据自己的数据
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    model.to(args.device)
    criterion = nn.MSELoss()  # 定义损失函数
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # Adam梯度下降  学习率=0.001


    #加载热导率数据
    train_loader, test_loader = getData_heat_conductivity(args.metalFile,args.sequence_length,args.batch_size)
    for i in range(50000):
        total_loss = 0
        for idx, (data, label) in enumerate(train_loader):

            if args.useGPU:
                print('使用gpu进行运算：')
                data1 = data.cuda()
                pred = model(Variable(data1).cuda())
                # print(pred.shape)
                pred = pred[1,:,:]
                label = label.unsqueeze(1).cuda()
                # print(label.shape)
            else:

                # data1 = data.squeeze(1)
                data1 = data

                #带入模型得出当前预测值
                pred = model(Variable(data1))
                pred = pred[1, :, :]
                label = label.unsqueeze(1)

            #目标优化函数 label是真实y pred是预测的y
            loss = criterion(pred, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            #损失tensor转为值
            total_loss += loss.item()
        print('当前损失为'+str(total_loss))
        viz.line([total_loss], [i], win='train_loss_h', update='append')
        if i % 10 == 0:
            # torch.save(model, args.save_file)
            torch.save({'state_dict': model.state_dict()}, args.save_file_heat_conductivity)
            print('第%d epoch，保存模型' % i)
    # torch.save(model, args.save_file)
    torch.save({'state_dict': model.state_dict()}, args.save_file_heat_conductivity)

#训练导电率网络
def trainConductivity():
    print('开始训练导电率网络')
    viz = Visdom()
    viz.line([0.], [0.], win='train_loss_c', opts=dict(title='train loss c'))

    #更改输入的size 根据自己的数据
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    model.to(args.device)
    criterion = nn.MSELoss()  # 定义损失函数
    optimizer = torch.optim.Adam(model.parameters(), lr=1)  # Adam梯度下降  学习率=0.001


    #加载导电率数据
    train_loader, test_loader = getDataConductivity(args.metalFile,args.sequence_length,args.batch_size)
    for i in range(50000):
        total_loss = 0
        for idx, (data, label) in enumerate(train_loader):
            if args.useGPU:
                data1 = data.squeeze(1).cuda()
                pred = model(Variable(data1).cuda())
                # print(pred.shape)
                pred = pred[1,:,:]
                label = label.unsqueeze(1).cuda()
                # print(label.shape)
            else:

                # data1 = data.squeeze(1)
                data1 = data

                #带入模型得出当前预测值
                pred = model(Variable(data1))
                pred = pred[1, :, :]
                label = label.unsqueeze(1)

            #目标优化函数 label是真实y pred是预测的y
            loss = criterion(pred, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print('当前损失为'+str(total_loss))
        viz.line([total_loss], [i], win='train_loss_c', update='append')
        if i % 10 == 0:
            # torch.save(model, args.save_file)
            torch.save({'state_dict': model.state_dict()}, args.save_file_conductivity)
            print('第%d epoch，保存模型' % i)
    # torch.save(model, args.save_file)
    torch.save({'state_dict': model.state_dict()}, args.save_file_conductivity)

#训练硬度网络
def trainSolidity():
    print('开始训练硬度网络')
    viz = Visdom()
    viz.line([0.], [0.], win='train_loss_s', opts=dict(title='train loss s'))

    #更改输入的size 根据自己的数据
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    model.to(args.device)
    criterion = nn.MSELoss()  # 定义损失函数
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # Adam梯度下降  学习率=0.001


    #加载硬度数据
    train_loader, test_loader = getDataSolidity(args.metalFile,args.sequence_length,args.batch_size)
    for i in range(50000):
        total_loss = 0
        for idx, (data, label) in enumerate(train_loader):
            if args.useGPU:
                data1 = data.squeeze(1).cuda()
                pred = model(Variable(data1).cuda())
                # print(pred.shape)
                pred = pred[1,:,:]
                label = label.unsqueeze(1).cuda()
                # print(label.shape)
            else:

                # data1 = data.squeeze(1)
                data1 = data

                #带入模型得出当前预测值
                pred = model(Variable(data1))
                pred = pred[1, :, :]
                label = label.unsqueeze(1)

            #目标优化函数 label是真实y pred是预测的y
            loss = criterion(pred, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print('当前损失为'+str(total_loss))
        viz.line([total_loss], [i], win='train_loss_s', update='append')
        if i % 10 == 0:
            # torch.save(model, args.save_file)
            torch.save({'state_dict': model.state_dict()}, args.save_file_solidity)
            print('第%d epoch，保存模型' % i)
    # torch.save(model, args.save_file)
    torch.save({'state_dict': model.state_dict()}, args.save_file_solidity)

#训练粘度网络
def trainViscosity():
    print('开始训练粘度网络')
    viz = Visdom()
    viz.line([0.], [0.], win='train_loss_v', opts=dict(title='train loss v'))

    #更改输入的size 根据自己的数据
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    model.to(args.device)
    criterion = nn.MSELoss()  # 定义损失函数
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # Adam梯度下降  学习率=0.001


    #加载硬度数据
    train_loader, test_loader = getDataViscosity(args.metalFile,args.sequence_length,args.batch_size)
    for i in range(50000):
        total_loss = 0
        for idx, (data, label) in enumerate(train_loader):
            if args.useGPU:
                data1 = data.squeeze(1).cuda()
                pred = model(Variable(data1).cuda())
                # print(pred.shape)
                pred = pred[1,:,:]
                label = label.unsqueeze(1).cuda()
                # print(label.shape)
            else:

                # data1 = data.squeeze(1)
                data1 = data

                #带入模型得出当前预测值
                pred = model(Variable(data1))
                pred = pred[1, :, :]
                label = label.unsqueeze(1)

            #目标优化函数 label是真实y pred是预测的y
            loss = criterion(pred, label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print('当前损失为'+str(total_loss))
        viz.line([total_loss], [i], win='train_loss_v', update='append')
        if i % 10 == 0:
            # torch.save(model, args.save_file)
            torch.save({'state_dict': model.state_dict()}, args.save_file_viscosity)
            print('第%d epoch，保存模型' % i)
    # torch.save(model, args.save_file)
    torch.save({'state_dict': model.state_dict()}, args.save_file_viscosity)


# train()

# trainDensity()
# train_heat_conductivity()
# trainConductivity()
# trainSolidity()
trainViscosity()