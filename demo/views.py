from django.shortcuts import render
import json
import os
# Create your views here.
from django.http import HttpResponse
from predict_project.predict import predict_viscosity,predict_solidity,predict_density,predict_conductivity,predict_heat_conductivity
from demo.tools.read_file import read_file
from predict_project.evaluate import evalDensity,eval_solidity,eval_conductivity,eval_heat_conductivity,eval_viscosity

from torch.autograd import Variable
import torch.nn as nn
import torch
from predict_project.LSTMModel import lstm
from predict_project.parser_my import args
from predict_project.dataset import getData,getDataDensity,getDataSolidity,getDataViscosity,getData_heat_conductivity,getDataConductivity
from visdom import Visdom
import time
import datetime


def detact(request):
    print('打开摄像头')
    return HttpResponse('打开了摄像头')

def camara_off(request):
    print('关闭了摄像头')
    return HttpResponse('关闭了摄像头')

def index(request):
    # 获取文件路径
    path = os.path.abspath('./predict_project/data/total.csv')
    # print(path)
    views_list = read_file(path)

    #对字典进行键值对处理，方便前端调用
    for i in range(len(views_list)):
        views_list[i]["密度"] = views_list[i].pop("密度 (g/cm3)")
        views_list[i]["电导率"] = views_list[i].pop("电导率（S/m）")
        views_list[i]["硬度"] = views_list[i].pop("硬度（HB）")
        views_list[i]["粘度"] = views_list[i].pop("粘度 (Pa.s)")
        views_list[i]["热导率"] = views_list[i].pop("热导率W/(m*K)")

    item_list = list(views_list[0].keys())
    print(views_list[0])
    return render(request,'index.html',{"views_list":views_list,"item_list":item_list})

#终身学习页面
def train_platform(request):

    back_path = os.path.abspath('./predict_project/backup/')

    #备份文件列表
    back_list = os.listdir(back_path)
    print(back_list)

    return render(request,"train_platform.html",{"back_list":back_list,})

#传送参数
def model(request):

    #加载的密度模型
    global model_density

    #密度模型的位置
    backup_path_density = os.path.abspath('./predict_project/backup/') +'/' + model_density

    data = json.loads(request.body)
    print(data)
    Ga = float(data['Ga'])
    In = float(data['In'])
    Al = float(data['Al'])
    Fe = float(data['Fe'])
    Co = float(data['Co'])
    Ni = float(data['Ni'])
    Cu = float(data['Cu'])
    Zn = float(data['Zn'])
    Mg = float(data['Mg'])
    Ag = float(data['Ag'])
    Bi = float(data['Bi'])
    Sn = float(data['Sn'])

    #预测的性能字典
    performance = {}

    #粘度
    viscosity = predict_viscosity(Mg,Al,Fe,Co,Ni,Cu,Zn,Ga,Ag,In,Sn,Bi)
    performance['viscosity'] = viscosity

    #密度
    if model_density=='':
        density = predict_density(Mg,Al,Fe,Co,Ni,Cu,Zn,Ga,Ag,In,Sn,Bi)
        print('加载的模型为：'+str(model_density))
    else:
        density = predict_density(Mg,Al,Fe,Co,Ni,Cu,Zn,Ga,Ag,In,Sn,Bi,backup_path_density)
        print('加载的模型为：' + str(backup_path_density))


    performance['density'] = density

    #热导率
    heat_conductivitys = predict_heat_conductivity(Mg,Al,Fe,Co,Ni,Cu,Zn,Ga,Ag,In,Sn,Bi)
    performance['heat_conductivitys'] = heat_conductivitys

    #电导率
    conductivity = predict_conductivity(Mg,Al,Fe,Co,Ni,Cu,Zn,Ga,Ag,In,Sn,Bi)
    performance['conductivity'] = conductivity

    #硬度
    solidity = predict_solidity(Mg,Al,Fe,Co,Ni,Cu,Zn,Ga,Ag,In,Sn,Bi)
    performance['solidity'] = solidity

    print(performance)
    # return render(request,'index.html')
    return HttpResponse(json.dumps(performance))


#返回测试函数
def eva(request):

    body = json.loads(request.body)
    model_name = body['model_name']
    print(model_name)
    global model_density

    backup_path_model = os.path.abspath('./predict_project/backup/') + '/' + model_density


    if model_name == 'density':
        if model_density == '':
            preds, lables, R2, M_loss = evalDensity()
        else:
            preds, lables, R2, M_loss = evalDensity(backup_path_model)
        result = {"preds": preds, "lables": lables, "R2": R2, "M_loss": M_loss}

    elif model_name == 'viscosity':
        preds, lables, R2, M_loss = eval_viscosity(backup_path_model)
        result = {"preds": preds, "lables": lables, "R2": R2, "M_loss": M_loss}

    elif model_name == 'solidity':
        preds, lables, R2, M_loss = eval_solidity(backup_path_model)
        result = {"preds": preds, "lables": lables, "R2": R2, "M_loss": M_loss}

    elif model_name == 'conductivity':
        preds, lables, R2, M_loss = eval_conductivity(backup_path_model)
        result = {"preds": preds, "lables": lables, "R2": R2, "M_loss": M_loss}

    elif model_name == 'heat_conductivity':
        preds, lables, R2, M_loss = eval_heat_conductivity(backup_path_model)
        result = {"preds": preds, "lables": lables, "R2": R2, "M_loss": M_loss}

    return HttpResponse(json.dumps(result))


#用于返回监控数据
result_density = {'log':[],'epoch':[],'time':[],'data_num':[],}

#不断取走监控数据返回前端
def monitor(request):

    global result_density
    print(result_density)
    return_result =  result_density
    result_density = {'log':[],'epoch':[],'time':[],'data_num':[]}
    return HttpResponse(json.dumps(return_result))

#控制训练开关
swicth = True

backup = False

#训练密度
def train_density(request):

    #用于保存全局监控数据
    global result_density
    global swicth
    global backup

    #打开训练阀门
    swicth = True








    # viz = Visdom()
    # viz.line([0.], [0.], win='train_loss_d', opts=dict(title='train loss d'))
    # print('开始训练密度网络')
    #
    # #更改输入的size 根据自己的数据
    # model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    # model.to(args.device)
    # criterion = nn.MSELoss()  # 定义损失函数
    # optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # Adam梯度下降  学习率=0.001
    #
    #
    # #加载密度数据
    # train_loader, test_loader,data_num = getDataDensity(args.metalFile,args.sequence_length,args.batch_size)
    #
    #
    # #计时器 捕获当前时间
    # time_start = time.time()  # 开始计时
    # for i in range(10000):
    #     total_loss = 0
    #
    #     #关闭训练
    #     if(swicth==False):
    #         break
    #     for idx, (data, label) in enumerate(train_loader):
    #
    #         #关闭训练
    #         if(swicth==False):
    #             break
    #
    #         if args.useGPU:
    #             print('使用gpu进行运算')
    #             data1 = data.cuda()
    #             pred = model(Variable(data1).cuda())
    #             # print(pred.shape)
    #             pred = pred[1,:,:]
    #             label = label.unsqueeze(1).cuda()
    #             # print(label.shape)
    #         else:
    #
    #             # data1 = data.squeeze(1)
    #             data1 = data
    #
    #             #带入模型得出当前预测值
    #             pred = model(Variable(data1))
    #             pred = pred[1, :, :]
    #             label = label.unsqueeze(1)
    #
    #         #目标优化函数 label是真实y pred是预测的y
    #         loss = criterion(pred, label)
    #         optimizer.zero_grad()
    #         loss.backward()
    #         optimizer.step()
    #         total_loss += loss.item()
    #
    #
    #     viz.line([total_loss], [i], win='train_loss_d', update='append')
    #
    #     #打印当前损失  添加损失日志到全局监控变量
    #     log = '当前损失为'+str(total_loss)
    #     print(log)
    #     result_density['log'].append(log)
    #
    #
    #     result_density['epoch'].append(i)
    #
    #     time_end = time.time()  # 结束计时
    #
    #     time_train = int(time_end - time_start)
    #
    #     result_density['time'].append(time_train)
    #
    #     result_density['data_num'].append(data_num)
    #
    #     if i % 10 == 0:
    #         # torch.save(model, args.save_file)
    #         torch.save({'state_dict': model.state_dict()}, args.save_file_density)
    #         print('第%d epoch，保存模型' % i)
    #
    #     if(backup == True):
    #
    #         #关闭备份开关
    #         backup=False
    #         year = datetime.datetime.now().year
    #         month = datetime.datetime.now().month
    #         day = datetime.datetime.now().day
    #         hour = datetime.datetime.now().hour
    #         minute = datetime.datetime.now().minute
    #         second = datetime.datetime.now().second
    #
    #         time_now = str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)
    #
    #         abpath = os.path.abspath('.')
    #         backup_path = abpath + '\predict_project\\backup\\'
    #
    #         #存取模型的绝对路径
    #         backup_abpath = backup_path + 'metal_density' + time_now +'.pkl'
    #         print(backup_abpath)
    #
    #         torch.save({'state_dict': model.state_dict()},backup_abpath)
    #
    #         print('备份成功！')
    #
    # # torch.save(model, args.save_file)
    # torch.save({'state_dict': model.state_dict()}, args.save_file_density)
    # print(model_density)




    #训练结果可视化
    viz = Visdom()
    viz.line([0.], [0.], win='train_loss', opts=dict(title='train loss'))

    model = lstm(input_size=args.input_size, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1, dropout=args.dropout, batch_first=args.batch_first )
    model.to(args.device)
    criterion = nn.MSELoss()  # 定义损失函数
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)  # Adam梯度下降  学习率=0.001

    close_max, close_min, train_loader, test_loader,data_num = getData(args.corpusFile,args.sequence_length,args.batch_size )


    #计时器 捕获当前时间
    time_start = time.time()  # 开始计时
    #训练开始
    for i in range(args.epochs):

        total_loss = 0

        # 跳出循环
        if (swicth == False):
            break

        for idx, (data, label) in enumerate(train_loader):

            #跳出循环
            if (swicth == False):
                break

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



        #打印当前损失  添加损失日志到全局监控变量
        log = '当前损失为'+str(total_loss)
        print(log)
        result_density['log'].append(log)

        result_density['data_num'].append(44)

        result_density['epoch'].append(i)

        time_end = time.time()  # 结束计时

        time_train = int(time_end - time_start)

        result_density['time'].append(time_train)

        if i % 10 == 0:
            # torch.save(model, args.save_file)
            torch.save({'state_dict': model.state_dict()}, args.save_file)
            print('第%d epoch，保存模型' % i)




        if(backup == True):

            #关闭备份开关
            backup=False
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            day = datetime.datetime.now().day
            hour = datetime.datetime.now().hour
            minute = datetime.datetime.now().minute
            second = datetime.datetime.now().second

            time_now = str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)

            abpath = os.path.abspath('.')
            backup_path = abpath + '\predict_project\\backup\\'

            #存取模型的绝对路径
            backup_abpath = backup_path + 'metal_density' + time_now +'.pkl'
            print(backup_abpath)

            torch.save({'state_dict': model.state_dict()},backup_abpath)

            print('备份成功！')



    # torch.save(model, args.save_file)
    torch.save({'state_dict': model.state_dict()}, args.save_file)

    return HttpResponse(1)

#控制训练开关关
def hanshu(request):
    global swicth

    #接收前端传来的关闭指令
    body = json.loads(request.body)
    swicth = body['switch']
    print(body['switch'])

    return HttpResponse("ok")

#控制训练开关闭
def backup(request):
    global backup

    backup = True
    print('打开备份开关,文件存在：')


    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second

    time_now = str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)

    abpath = os.path.abspath('.')
    backup_path = abpath + '\predict_project\\backup\\'

    # 存取模型的绝对路径
    backup_abpath = backup_path + 'metal_density' + time_now + '.pkl'
    print(backup_abpath)


    return HttpResponse("ok")

#选择的模型
model_density = ''

#模型加载
def model_load(request):
    global model_density
    body = request.body
    body = json.loads(body)
    print(body)
    model_density = body['model']
    print(model_density)
    return HttpResponse('ok')