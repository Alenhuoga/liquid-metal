from pandas import read_csv
import numpy as np
from torch.utils.data import DataLoader,Dataset
import torch
from torchvision import transforms
from predict_project.parser_my import args
#
def getData(corpusFile,sequence_length,batchSize):

    # 数据预处理 ，去除id、股票代码、前一天的收盘价、交易日期等对训练无用的无效数据
    #读取数据
    stock_data = read_csv(corpusFile)
    #打出数据集望望
    # print(stock_data)
    stock_data.drop('ts_code', axis=1, inplace=True)  # 删除第二列’股票代码‘ axis删除列
    stock_data.drop('id', axis=1, inplace=True)  # 删除第一列’id‘
    stock_data.drop('pre_close', axis=1, inplace=True)  # 删除列’pre_close‘
    stock_data.drop('trade_date', axis=1, inplace=True)  # 删除列’trade_date‘



    close_max = stock_data['close'].max() #收盘价的最大值
    close_min = stock_data['close'].min() #收盘价的最小值
    df = stock_data.apply(lambda x: (x - min(x)) / (max(x) - min(x)))  # min-max标准化
    print('之后：' + str(df))
    # 构造X和Y
    #根据前n天的数据，预测未来一天的收盘价(close)， 例如：根据1月1日、1月2日、1月3日、1月4日、1月5日的数据（每一天的数据包含8个特征），预测1月6日的收盘价。
    sequence = sequence_length
    X = []
    Y = []
    for i in range(df.shape[0] - sequence):
        X.append(np.array(df.iloc[i:(i + sequence), ].values, dtype=np.float32))
        Y.append(np.array(df.iloc[(i + sequence), 0], dtype=np.float32))

    print(X)
    # 构建batch
    total_len = len(Y)
    # print(total_len)

    trainx, trainy = X[:int(0.99 * total_len)], Y[:int(0.99 * total_len)]
    testx, testy = X[int(0.7 * total_len):], Y[int(0.7 * total_len):]




    # print(trainx)


    #获得训练集
    train_loader = DataLoader(dataset=Mydataset(trainx, trainy, transform=transforms.ToTensor()), batch_size=batchSize,
                              shuffle=True)
    #获得测试集 用Mydataset获得x 和 y
    test_loader = DataLoader(dataset=Mydataset(testx, testy), batch_size=batchSize, shuffle=True)
    return close_max,close_min,train_loader,test_loader,total_len



#热导率模型数据
def getData_heat_conductivity(corpusFile,sequence_length,batchSize):


    #读取数据
    stock_data = read_csv(corpusFile,encoding='gb18030')
    #打出数据集望望
    print(stock_data)
    stock_data.drop('序号', axis=1, inplace=True)  # 删除序号
    stock_data.drop('检测编号', axis=1, inplace=True)#删除检测编号
    stock_data.drop('备注', axis=1, inplace=True)  # 删除备注
    stock_data.drop('求和', axis=1, inplace=True)  # 删除备注

    stock_data.drop('密度 (g/cm3)',axis=1, inplace=True)#删除输出属性
    stock_data.drop('电导率（S/m）', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('硬度（HB）', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('粘度 (Pa.s)', axis=1, inplace=True)  # 删除输出属性


    #删除密度中nan的行
    stock_data = stock_data.dropna(axis=0,how='any')



    print('之后\n'+str(stock_data))
    #pandas shape返回几行几列 0是行 1是列
    df = stock_data
    print(df.shape[0])

    # 构造X和Y
    #根据前n天的数据，预测未来一天的收盘价(close)， 例如：根据1月1日、1月2日、1月3日、1月4日、1月5日的数据（每一天的数据包含8个特征），预测1月6日的收盘价。
    sequence = sequence_length
    X = []
    Y = []

    #iloc取行
    for i in range(df.shape[0]):

        X.append(np.array(df.iloc[i:(i + 1), 0:12].values, dtype=np.float32))
        Y.append(np.array(df.iloc[(i), 12], dtype=np.float32))

    # 构建batch
    total_len = len(Y)
    data_num = total_len

    #划分测试集和训练集
    trainx, trainy = X[:int(0.99 * total_len)], Y[:int(0.99 * total_len)]
    testx, testy = X[int(0.7 * total_len):], Y[int(0.7 * total_len):]

    print(X)

    print(Y)
    print('数据量为：' + str(total_len))


    #获得训练集
    # train_loader = DataLoader(dataset=Mydataset(X, Y, transform=transforms.ToTensor()), batch_size=batchSize,
    #                           shuffle=True)

    train_loader = DataLoader(dataset=Mydataset(X, Y, transform=None), batch_size=batchSize,
                              shuffle=True)
    #获得测试集
    test_loader = DataLoader(dataset=Mydataset(testx, testy), batch_size=batchSize, shuffle=True)
    return train_loader,test_loader,data_num


#密度模型数据
def getDataDensity(corpusFile,sequence_length,batchSize):


    #读取数据
    stock_data = read_csv(corpusFile,encoding='gb18030')
    #打出数据集望望
    print(stock_data)
    stock_data.drop('序号', axis=1, inplace=True)  # 删除序号
    stock_data.drop('检测编号', axis=1, inplace=True)#删除检测编号
    stock_data.drop('备注', axis=1, inplace=True)  # 删除备注
    stock_data.drop('求和', axis=1, inplace=True)  # 删除备注

    stock_data.drop('热导率W/(m*K)',axis=1, inplace=True)#删除输出属性
    stock_data.drop('电导率（S/m）', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('硬度（HB）', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('粘度 (Pa.s)', axis=1, inplace=True)  # 删除输出属性


    #删除密度中nan的行
    stock_data = stock_data.dropna(axis=0,how='any')



    print('之后\n'+str(stock_data))
    #pandas shape返回几行几列 0是行 1是列
    df = stock_data
    print(df.shape[0])

    # 构造X和Y
    #根据前n天的数据，预测未来一天的收盘价(close)， 例如：根据1月1日、1月2日、1月3日、1月4日、1月5日的数据（每一天的数据包含8个特征），预测1月6日的收盘价。
    sequence = sequence_length
    X = []
    Y = []

    #iloc取行
    for i in range(df.shape[0]):

        X.append(np.array(df.iloc[i:(i + 1), 0:12].values, dtype=np.float32))
        Y.append(np.array(df.iloc[(i), 12], dtype=np.float32))

    # 构建batch
    total_len = len(Y)


    #划分测试集和训练集
    trainx, trainy = X[:int(0.99 * total_len)], Y[:int(0.99 * total_len)]
    testx, testy = X[int(0.7 * total_len):], Y[int(0.7 * total_len):]

    print(X)
    # print('x的尺寸为：'+str(X.size()))
    print(Y)
    print('数据量为：' + str(total_len))
    data_num = total_len

    #获得训练集
    # train_loader = DataLoader(dataset=Mydataset(X, Y, transform=transforms.ToTensor()), batch_size=batchSize,
    #                           shuffle=True)

    train_loader = DataLoader(dataset=Mydataset(X, Y, transform=None), batch_size=batchSize,
                              shuffle=True)
    #获得测试集
    test_loader = DataLoader(dataset=Mydataset(testx, testy), batch_size=batchSize, shuffle=True)
    return train_loader,test_loader,data_num


#电导率属性数据
def getDataConductivity(corpusFile,sequence_length,batchSize):


    #读取数据
    stock_data = read_csv(corpusFile,encoding='gb18030')
    #打出数据集望望
    print(stock_data)
    stock_data.drop('序号', axis=1, inplace=True)  # 删除序号
    stock_data.drop('检测编号', axis=1, inplace=True)#删除检测编号
    stock_data.drop('备注', axis=1, inplace=True)  # 删除备注
    stock_data.drop('求和', axis=1, inplace=True)  # 删除备注

    stock_data.drop('热导率W/(m*K)',axis=1, inplace=True)#删除输出属性
    stock_data.drop('密度 (g/cm3)', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('硬度（HB）', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('粘度 (Pa.s)', axis=1, inplace=True)  # 删除输出属性


    #删除密度中nan的行
    stock_data = stock_data.dropna(axis=0,how='any')



    print('之后\n'+str(stock_data))
    #pandas shape返回几行几列 0是行 1是列
    df = stock_data
    print(df.shape[0])

    # 构造X和Y
    #根据前n天的数据，预测未来一天的收盘价(close)， 例如：根据1月1日、1月2日、1月3日、1月4日、1月5日的数据（每一天的数据包含8个特征），预测1月6日的收盘价。
    sequence = sequence_length
    X = []
    Y = []

    #iloc取行
    for i in range(df.shape[0]):

        X.append(np.array(df.iloc[i:(i + 1), 0:12].values, dtype=np.float32))
        Y.append(np.array(df.iloc[(i), 12], dtype=np.float32))

    # 构建batch
    total_len = len(Y)
    data_num = total_len

    #划分测试集和训练集
    trainx, trainy = X[:int(0.99 * total_len)], Y[:int(0.99 * total_len)]
    testx, testy = X[int(0.7 * total_len):], Y[int(0.7 * total_len):]

    print(X)

    print(Y)
    print('数据量为：'+str(total_len))


    #获得训练集
    # train_loader = DataLoader(dataset=Mydataset(X, Y, transform=transforms.ToTensor()), batch_size=batchSize,
    #                           shuffle=True)

    train_loader = DataLoader(dataset=Mydataset(X, Y, transform=None), batch_size=batchSize,
                              shuffle=True)
    #获得测试集
    test_loader = DataLoader(dataset=Mydataset(testx, testy), batch_size=batchSize, shuffle=True)
    return train_loader,test_loader,data_num


#硬度属性数据
def getDataSolidity(corpusFile,sequence_length,batchSize):


    #读取数据
    stock_data = read_csv(corpusFile,encoding='gb18030')
    #打出数据集望望
    print(stock_data)
    stock_data.drop('序号', axis=1, inplace=True)  # 删除序号
    stock_data.drop('检测编号', axis=1, inplace=True)#删除检测编号
    stock_data.drop('备注', axis=1, inplace=True)  # 删除备注
    stock_data.drop('求和', axis=1, inplace=True)  # 删除备注

    stock_data.drop('热导率W/(m*K)',axis=1, inplace=True)#删除输出属性
    stock_data.drop('密度 (g/cm3)', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('电导率（S/m）', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('粘度 (Pa.s)', axis=1, inplace=True)  # 删除输出属性


    #删除密度中nan的行
    stock_data = stock_data.dropna(axis=0,how='any')



    print('之后\n'+str(stock_data))
    #pandas shape返回几行几列 0是行 1是列
    df = stock_data
    print(df.shape[0])

    # 构造X和Y
    #根据前n天的数据，预测未来一天的收盘价(close)， 例如：根据1月1日、1月2日、1月3日、1月4日、1月5日的数据（每一天的数据包含8个特征），预测1月6日的收盘价。
    sequence = sequence_length
    X = []
    Y = []

    #iloc取行
    for i in range(df.shape[0]):

        X.append(np.array(df.iloc[i:(i + 1), 0:12].values, dtype=np.float32))
        Y.append(np.array(df.iloc[(i), 12], dtype=np.float32))

    # 构建batch
    total_len = len(Y)
    data_num = total_len

    #划分测试集和训练集
    trainx, trainy = X[:int(0.99 * total_len)], Y[:int(0.99 * total_len)]
    testx, testy = X[int(0.7 * total_len):], Y[int(0.7 * total_len):]

    print(X)

    print(Y)
    print('数据量为：'+str(total_len))


    #获得训练集
    # train_loader = DataLoader(dataset=Mydataset(X, Y, transform=transforms.ToTensor()), batch_size=batchSize,
    #                           shuffle=True)

    train_loader = DataLoader(dataset=Mydataset(X, Y, transform=None), batch_size=batchSize,
                              shuffle=True)
    #获得测试集
    test_loader = DataLoader(dataset=Mydataset(testx, testy), batch_size=batchSize, shuffle=True)
    return train_loader,test_loader,data_num

#粘度模型数据
def getDataViscosity(corpusFile,sequence_length,batchSize):


    #读取数据
    stock_data = read_csv(corpusFile,encoding='gb18030')
    #打出数据集望望
    print(stock_data)
    stock_data.drop('序号', axis=1, inplace=True)  # 删除序号
    stock_data.drop('检测编号', axis=1, inplace=True)#删除检测编号
    stock_data.drop('备注', axis=1, inplace=True)  # 删除备注
    stock_data.drop('求和', axis=1, inplace=True)  # 删除备注

    stock_data.drop('热导率W/(m*K)',axis=1, inplace=True)#删除输出属性
    stock_data.drop('电导率（S/m）', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('硬度（HB）', axis=1, inplace=True)  # 删除输出属性
    stock_data.drop('密度 (g/cm3)', axis=1, inplace=True)  # 删除输出属性


    #删除密度中nan的行
    stock_data = stock_data.dropna(axis=0,how='any')



    print('之后\n'+str(stock_data))
    #pandas shape返回几行几列 0是行 1是列
    df = stock_data
    print(df.shape[0])

    # 构造X和Y
    #根据前n天的数据，预测未来一天的收盘价(close)， 例如：根据1月1日、1月2日、1月3日、1月4日、1月5日的数据（每一天的数据包含8个特征），预测1月6日的收盘价。
    sequence = sequence_length
    X = []
    Y = []

    #iloc取行
    for i in range(df.shape[0]):

        X.append(np.array(df.iloc[i:(i + 1), 0:12].values, dtype=np.float32))
        Y.append(np.array(df.iloc[(i), 12], dtype=np.float32))

    # 构建batch
    total_len = len(Y)
    data_num = total_len

    #划分测试集和训练集  随机打散后 前几条是是训练集 后面几条是测试集
    trainx, trainy = X[:int(0.99 * total_len)], Y[:int(0.99 * total_len)]
    testx, testy = X[int(0.7 * total_len):], Y[int(0.7 * total_len):]

    print(X)

    print(Y)
    print('数据量为：' + str(total_len))


    #获得训练集
    # train_loader = DataLoader(dataset=Mydataset(X, Y, transform=transforms.ToTensor()), batch_size=batchSize,
    #                           shuffle=True)

    train_loader = DataLoader(dataset=Mydataset(X, Y, transform=None), batch_size=batchSize,
                              shuffle=True)
    #获得测试集
    test_loader = DataLoader(dataset=Mydataset(testx, testy), batch_size=batchSize, shuffle=True)
    return train_loader,test_loader,data_num



class Mydataset(Dataset):
    def __init__(self, xx, yy, transform=None):
        self.x = xx
        self.y = yy
        self.tranform = transform

    def __getitem__(self, index):
        x1 = self.x[index]
        y1 = self.y[index]
        if self.tranform != None:
            return self.tranform(x1), y1
        return x1, y1

    def __len__(self):
        return len(self.x)



#看下预处理数据
# getData(args.corpusFile,args.sequence_length,args.batch_size )

#getDataDensity(args.metalFile,args.sequence_length,args.batch_size)

#getData_heat_conductivity(args.metalFile,args.sequence_length,args.batch_size)

#getDataConductivity(args.metalFile,args.sequence_length,args.batch_size)

#getDataSolidity(args.metalFile,args.sequence_length,args.batch_size)

# getDataViscosity(args.metalFile,args.sequence_length,args.batch_size)