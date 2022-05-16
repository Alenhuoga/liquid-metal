from predict_project.LSTMModel import lstm
from predict_project.dataset import getData,getDataDensity,getDataSolidity,getDataViscosity,getData_heat_conductivity,getDataConductivity
from predict_project.parser_my import args
import torch
import os


#r2_score
def r2_loss(output, target):
    target_mean = torch.mean(target)
    ss_tot = torch.sum((target - target_mean) ** 2)
    ss_res = torch.sum((target - output) ** 2)
    r2 = 1 - ss_res / ss_tot
    return r2

#SE 两数平方差
def se_loss(pred,lable):
    return abs(pred-lable)**2


def eval():
    # model = torch.load(args.save_file)
    model = lstm(input_size=args.input_size, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    #加载模型 进行预测
    checkpoint = torch.load(args.save_file)
    model.load_state_dict(checkpoint['state_dict'])
    preds = []
    labels = []
    close_max, close_min, train_loader, test_loader = getData(args.corpusFile, args.sequence_length, args.batch_size)
    for idx, (x, label) in enumerate(test_loader):
        if args.useGPU:
            x = x.squeeze(1).cuda()  # batch_size,seq_len,input_size
        else:
            x = x.squeeze(1)

        print('打出来看看'+str(x)+'类型是')
        #进行预测
        pred = model(x)
        list = pred.data.squeeze(1).tolist()
        preds.extend(list[-1])
        labels.extend(label.tolist())
    print('预测的label是'+str(label))

    #循环预测
    # for i in range(len(preds)):
    #     print('预测值是%.2f,真实值是%.2f' % (
    #     preds[i][0] * (close_max - close_min) + close_min, labels[i] * (close_max - close_min) + close_min))

def evalDensity(model_name =args.save_file_density):
    # model = torch.load(args.save_file)
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    #加载模型 进行预测
    checkpoint = torch.load(model_name)

    model.load_state_dict(checkpoint['state_dict'])
    preds = []
    labels = []


    train_loader, test_loader ,data_num = getDataDensity(args.metalFile, args.sequence_length, args.batch_size)
    for idx, (x, label) in enumerate(test_loader):
        if args.useGPU:
            x = x.cuda()  # batch_size,seq_len,input_size
        else:
            x = x

        print('输入的参数为'+str(x))
        print('输入的参数类别为' + str(x.type()))
        print('输入的尺寸为' + str(x.size()))
        #进行预测
        pred = model(x)
        list = pred.data.squeeze(1).tolist()
        preds.extend(list[-1])
        labels.extend(label.tolist())


    for i in range(len(preds)):
        print('预测的密度是' + str(preds[i]))
        print('真实的密度是' + str(labels[i]))



    for i in range(len(preds)):
        print('真实的密度是' + str(labels[i]))
        print('预测的密度是' + str(preds[i][0]))

    #算损失
    total = 0
    loss = 0
    M_lable = 0
    total_lable = 0
    for i in range(len(preds)):
        loss = loss+se_loss(preds[i][0],labels[i])
        total = total+1
        total_lable = total_lable + labels[i]

    M_loss = loss/total
    M_lable = total_lable/total


    #R2
    SSR = 0
    SST = 0
    for i in range(len(preds)):

        SSR = (preds[i][0] - M_lable)**2+SSR
        SST = (labels[i] - M_lable)**2+SST

    R2 = SSR/SST
    print("R2为："+str(R2))
    print('总的损失为:'+str(M_loss))

    return preds,labels,R2,M_loss

def eval_heat_conductivity(model_name =args.save_file_heat_conductivity):
    # model = torch.load(args.save_file)
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    #加载模型 进行预测
    checkpoint = torch.load(model_name)

    model.load_state_dict(checkpoint['state_dict'])
    preds = []
    labels = []


    train_loader, test_loader ,data_num = getData_heat_conductivity(args.metalFile, args.sequence_length, args.batch_size)
    for idx, (x, label) in enumerate(test_loader):
        if args.useGPU:
            x = x.cuda()  # batch_size,seq_len,input_size
        else:
            x = x

        print('输入的参数为'+str(x))
        print('输入的参数类别为' + str(x.type()))
        print('输入的尺寸为' + str(x.size()))
        #进行预测
        pred = model(x)
        list = pred.data.squeeze(1).tolist()
        preds.extend(list[-1])
        labels.extend(label.tolist())


    for i in range(len(preds)):
        print('预测的热导率是' + str(preds[i]))
        print('真实的热导率是' + str(labels[i]))



    for i in range(len(preds)):
        print('真实的热导率是' + str(labels[i]))
        print('预测的热导率是' + str(preds[i][0]))

    #算损失
    total = 0
    loss = 0
    M_lable = 0
    total_lable = 0
    for i in range(len(preds)):
        loss = loss+se_loss(preds[i][0],labels[i])
        total = total+1
        total_lable = total_lable + labels[i]

    M_loss = loss/total
    M_lable = total_lable/total


    #R2
    SSR = 0
    SST = 0
    for i in range(len(preds)):

        SSR = (preds[i][0] - M_lable)**2+SSR
        SST = (labels[i] - M_lable)**2+SST

    R2 = SSR/SST
    print("R2为："+str(R2))
    print('总的损失为:'+str(M_loss))

    return preds,labels,R2,M_loss

def eval_conductivity(model_name =args.save_file_conductivity):
    # model = torch.load(args.save_file)
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    #加载模型 进行预测
    checkpoint = torch.load(model_name)

    model.load_state_dict(checkpoint['state_dict'])
    preds = []
    labels = []


    train_loader, test_loader ,data_num = getDataConductivity(args.metalFile, args.sequence_length, args.batch_size)
    for idx, (x, label) in enumerate(test_loader):
        if args.useGPU:
            x = x.cuda()  # batch_size,seq_len,input_size
        else:
            x = x

        print('输入的参数为'+str(x))
        print('输入的参数类别为' + str(x.type()))
        print('输入的尺寸为' + str(x.size()))
        #进行预测
        pred = model(x)
        list = pred.data.squeeze(1).tolist()
        preds.extend(list[-1])
        labels.extend(label.tolist())


    for i in range(len(preds)):
        print('预测的电导率是' + str(preds[i]))
        print('真实的电导率是' + str(labels[i]))



    for i in range(len(preds)):
        print('真实的电导率是' + str(labels[i]))
        print('预测的电导率是' + str(preds[i][0]))

    #算损失
    total = 0
    loss = 0
    M_lable = 0
    total_lable = 0
    for i in range(len(preds)):
        loss = loss+se_loss(preds[i][0],labels[i])
        total = total+1
        total_lable = total_lable + labels[i]

    M_loss = loss/total
    M_lable = total_lable/total


    #R2
    SSR = 0
    SST = 0
    for i in range(len(preds)):

        SSR = (preds[i][0] - M_lable)**2+SSR
        SST = (labels[i] - M_lable)**2+SST

    R2 = SSR/SST
    print("R2为："+str(R2))
    print('总的损失为:'+str(M_loss))

    return preds,labels,R2,M_loss

def eval_solidity(model_name =args.save_file_solidity):
    # model = torch.load(args.save_file)
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    #加载模型 进行预测
    checkpoint = torch.load(model_name)

    model.load_state_dict(checkpoint['state_dict'])
    preds = []
    labels = []


    train_loader, test_loader ,data_num = getDataSolidity(args.metalFile, args.sequence_length, args.batch_size)
    for idx, (x, label) in enumerate(test_loader):
        if args.useGPU:
            x = x.cuda()  # batch_size,seq_len,input_size
        else:
            x = x

        print('输入的参数为'+str(x))
        print('输入的参数类别为' + str(x.type()))
        print('输入的尺寸为' + str(x.size()))
        #进行预测
        pred = model(x)
        list = pred.data.squeeze(1).tolist()
        preds.extend(list[-1])
        labels.extend(label.tolist())


    for i in range(len(preds)):
        print('预测的硬度是' + str(preds[i]))
        print('真实的硬度是' + str(labels[i]))



    for i in range(len(preds)):
        print('真实的硬度是' + str(labels[i]))
        print('预测的硬度是' + str(preds[i][0]))

    #算损失
    total = 0
    loss = 0
    M_lable = 0
    total_lable = 0
    for i in range(len(preds)):
        loss = loss+se_loss(preds[i][0],labels[i])
        total = total+1
        total_lable = total_lable + labels[i]

    M_loss = loss/total
    M_lable = total_lable/total


    #R2
    SSR = 0
    SST = 0
    for i in range(len(preds)):

        SSR = (preds[i][0] - M_lable)**2+SSR
        SST = (labels[i] - M_lable)**2+SST

    R2 = SSR/SST
    print("R2为："+str(R2))
    print('总的损失为:'+str(M_loss))

    return preds,labels,R2,M_loss

def eval_viscosity(model_name =args.save_file_viscosity):
    # model = torch.load(args.save_file)
    #更改size 根据自己输入的属性
    model = lstm(input_size=12, hidden_size=args.hidden_size, num_layers=args.layers , output_size=1)
    model.to(args.device)

    #加载模型 进行预测
    checkpoint = torch.load(model_name)

    model.load_state_dict(checkpoint['state_dict'])
    preds = []
    labels = []


    train_loader, test_loader ,data_num = getDataViscosity(args.metalFile, args.sequence_length, args.batch_size)
    for idx, (x, label) in enumerate(test_loader):
        if args.useGPU:
            x = x.cuda()  # batch_size,seq_len,input_size
        else:
            x = x

        print('输入的参数为'+str(x))
        print('输入的参数类别为' + str(x.type()))
        print('输入的尺寸为' + str(x.size()))
        #进行预测
        pred = model(x)
        list = pred.data.squeeze(1).tolist()
        preds.extend(list[-1])
        labels.extend(label.tolist())


    for i in range(len(preds)):
        print('预测的粘度是' + str(preds[i]))
        print('真实的粘度是' + str(labels[i]))



    for i in range(len(preds)):
        print('真实的粘度是' + str(labels[i]))
        print('预测的粘度是' + str(preds[i][0]))

    #算损失
    total = 0
    loss = 0
    M_lable = 0
    total_lable = 0
    for i in range(len(preds)):
        loss = loss+se_loss(preds[i][0],labels[i])
        total = total+1
        total_lable = total_lable + labels[i]

    M_loss = loss/total
    M_lable = total_lable/total


    #R2
    SSR = 0
    SST = 0
    for i in range(len(preds)):

        SSR = (preds[i][0] - M_lable)**2+SSR
        SST = (labels[i] - M_lable)**2+SST

    R2 = SSR/SST
    print("R2为："+str(R2))
    print('总的损失为:'+str(M_loss))

    return preds,labels,R2,M_loss
# eval()
# evalDensity()