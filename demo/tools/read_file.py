from pandas import read_csv
import os

path = os.path.abspath('../../predict_project/data/total.csv')
def read_file(path):

    print(path)
    # 读取数据
    data = read_csv(path, encoding='gb18030',sep=',')
    data.drop('序号', axis=1, inplace=True)  # 删除序号

    data.drop('备注', axis=1, inplace=True)  # 删除备注
    data.drop('求和', axis=1, inplace=True)  # 删除备注
    data = data.to_dict(orient='records')
    print(data[0])
    # for i in data:
    #     print(i.keys())
    return data


# read_file(path)

# a = {"name":15,"as":1,"b":12
# }
# a["ax"] = a.pop("as")
# print(a)