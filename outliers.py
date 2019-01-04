#coding=utf8
# 一些数据预处理
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import os
import sys
import pickle
import argparse
import configparser

class Outliers:
    '''
    异常点检测类，包含读取、预处理、异常点检测等功能
    '''
    # 输入输出文件
    # 读入：本地的 csv 文件（已经计算过新的特征，只需要做一些数据填充），做异常点检测
    # 输出：检测结果（只包含时间戳、异常分数、异常结果三列）
    input_filename = 'data.csv'
    output_filename = 'outliers_result.csv'
    # 读入的原始数据
    origin_data = None
    # 需要考虑的特征
    field_list = [
        'retxclientRate', 'retxserverRate', 'zerowindowclientnum',
        'zerowindowservernum', 'transresptime', 'clientseglostRate', 'serverseglostRate',
    ]

    # 异常点检测参数
    # 树的数量
    n_estimators = 100
    # 离群点的比例
    contamination = 0.001
    # 预测时的批量大小
    batch = 256
    # 控制显示信息的冗长性
    verbose = 0

    # 模型保存/加载参数
    # 是否保存模型的开关，默认为False，即不保存模型；如果为True，则只训练，然后保存模型。
    isSaveModel = False
    # 是否加载模型的开关，默认为False，即不保存模型；如果为True，则只训练，然后保存模型。
    isLoadModel = False
    # 模型默认的保存名称，只有当 isOnlyTrain = True 时才保存模型
    modelname = 'IsolationForest.model'
    # output_filename = 'outliers_%s_2.csv'%(str(contamination))

    def __init__(self,  input_filename=None, output_filename=None, n_estimators=None, proportion=None, batch=None, verbose=None, 
                        issavemodel=None, isloadmodel=None, modelname=None):
        '''
        构造函数
        '''
        if input_filename:
            self.input_filename = input_filename
        if output_filename:
            self.output_filename = output_filename
        if n_estimators:
            self.n_estimators = n_estimators
        if proportion:
            self.contamination = proportion
        if batch:
            self.batch = batch
        if verbose:
            self.verbose = verbose
        if issavemodel:
            self.isSaveModel = issavemodel
        if isloadmodel:
            self.isLoadModel = isloadmodel
        if modelname:
            self.modelname = modelname

        self.read(input_filename)


    def read(self, filename=None):
        '''
        读取原始数据文件
        如果不指定 filename 参数，则默认读取 self.input_filename 定义的文件
        '''
        # 是否指定了输入文件
        if filename is None:
            filename = self.input_filename
            
        print('Reading `%s`...'%filename)

        # 判断文件是否存在
        if not os.path.exists(filename):
            raise Exception('File `%s` is not provided'%filename)

        # 读取原始数据
        self.origin_data = pd.read_csv(filename)

    def preprocess(self):
        '''
        数据预处理函数
        '''
        print('Data preprocessing...')
        if self.origin_data is None:
            # 原始数据是 None
            raise Exception('`self.origin_data` is None')

        # 预处理数据赋值
        data = self.origin_data

        # 填充缺失值
        data.fillna(0)

        # 计算 客户端重传率
        if 'retxclientRate' not in data.columns:
            data['retxclientRate'] = data['retxclientnum'] / data['totalclientpkts']

        # 计算 服务端重传率
        if 'retxserverRate' not in data.columns:
            data['retxserverRate'] = data['retxservernum'] / data['totalserverpkts']   

        # 客户端丢包率 和 服务端丢包率
        if 'clientseglostRate' not in data.columns:
            data['clientseglostRate'] = data['clientseglostnum'] / data['totalclientpkts']
        if 'serverseglostRate' not in data.columns:
            data['serverseglostRate'] = data['serverseglostnum'] / data['totalserverpkts']

        # 清洗数据，将所有无限值、nan 值替换为0
        data = data.replace((np.inf, -np.inf, np.nan), 0)

        # 取出数据中的上四分位数
        Q3 = float(data['transresptime'].quantile(0.75))
        # 填充该列所有小于上四分位数的值为上四分位数
        data.transresptime[data.transresptime < Q3] = Q3

        # 调整数值量级
        data['transresptime'] = data['transresptime'] / 1000

        # 选择包含 Rate 的字段，并调整他们的量级
        data.loc[:, data.columns.str.contains('\.?Rate')] = data.loc[:, data.columns.str.contains('\.?Rate')] * 10000

        # 提取需要的字段
        return data[self.field_list]

    def detect(self):
        '''
        利用孤立森林 isolation forest 进行离群点检测
        '''
        # 获得预处理之后的数据
        data = self.preprocess()

        # 异常点检测
        # 创建 IsolationForest
        ilf = IsolationForest(n_estimators=self.n_estimators,
                              n_jobs=-1,          # 使用全部cpu
                              verbose=self.verbose,
                              contamination = self.contamination, # 离群点的比例
                            )


        # 是否保存/加载模型的控制流
        if self.isSaveModel and self.isLoadModel:
            # isSaveModel = True & isLoadModel = True
            # 训练并保存模型到本地，然后继续预测
            # 训练
            print('Model training...')
            ilf.fit(data)
            # 保存模型到本地
            print('Saving model to `%s`...'%self.modelname)
            with open(self.modelname, 'wb') as fp:
                pickle.dump(ilf, fp)
        elif self.isSaveModel:
            # isSaveModel = True & isLoadModel = False
            # 训练并保存模型到本地，然后不再继续预测
            # 训练
            print('Model training...')
            ilf.fit(data)
            # 保存模型到本地
            print('Saving model to `%s`...'%self.modelname)
            with open(self.modelname, 'wb') as fp:
                pickle.dump(ilf, fp)
            print('Don\'t predict.')
            return 
        elif self.isLoadModel:
            # isSaveModel = False & isLoadModel = True
            # 直接加载本地模型，然后继续预测
            # 加载本地模型
            print('Loading model from `%s`...'%self.modelname)
            with open(self.modelname, 'rb') as fp:
                ilf = pickle.load(fp)
        else:
            # isSaveModel = False & isLoadModel = False
            # 只训练不保存模型，然后继续预测
            # 训练
            print('Model training...')
            ilf.fit(data)


        # 预测
        print('Outliers predicting...')
        shape = data.shape[0]
        all_pred = []
        all_score = []
        for i in range(int(shape/self.batch)+1):
            start = i * self.batch
            end = (i+1) * self.batch
            batch_test = data[start:end]
            # 预测
            # 返回值：+1 表示正常样本， -1表示异常样本
            pred = ilf.predict(batch_test)
            # 返回样本的异常评分。 值越小表示越有可能是异常样本
            score = ilf.decision_function(batch_test)
            all_pred.extend(pred)
            all_score.extend(score)

        data['timestamp'] = self.origin_data['timestamp']
        data['is_outlier'] = all_pred
        data['outlier_score'] = all_score

        print('Writing `%s`...'%self.output_filename)
        data.to_csv(self.output_filename, columns=['timestamp', 'outlier_score', 'is_outlier'], header=True, index=0)

def _parse_args():
    '''
    解析命令行参数
    '''
    parser = argparse.ArgumentParser(description='A outliers detect tool.')

    parser.add_argument('-i', '--input', dest='input_filename', action='store',
                        default='data.csv', type=str, help='specify the input file, default `data.csv`')

    parser.add_argument('-o', '--output', dest='output_filename', action='store',
                        default='outliers_result.csv', type=str, help='specify the output file, default `outliers_result.csv`')

    parser.add_argument('-n', '--n_estimators', dest='n_estimators', action='store',
                        default=100, type=int, help='the number of base estimators in the ensemble, default 100')

    parser.add_argument('-p', '--proportion', dest='proportion', action='store',
                        default=0.001, type=float, help='the proportion of outliers in the data set, default 0.001')

    parser.add_argument('-b', '--batch', dest='batch', action='store',
                        default=256, type=int, help='batch size for predicting, default 256')

    parser.add_argument('-v', '--verbose', dest='verbose', action='store',
                        default=0, type=int, help='controls the verbosity of the tree building process, default 0')

    parser.add_argument('-s', '--isSaveModel', dest='issavemodel', action='store_true',
                        default=False, help='whether to save the model after training. False (default) => train and predict, not save model. True => only train, then save the model')

    parser.add_argument('-l', '--isLoadModel', dest='isloadmodel', action='store_true',
                        default=False, help='whether to load the local model for prediction. False (default) => train and predict. True => load local model and predict')

    parser.add_argument('-m', '--model', dest='modelname', action='store',
                        default='IsolationForest.model', type=str, help='specify the saved model name, default `IsolationForest.model`')

    parser.add_argument('--ini', dest='config_filename', action='store',
                        default=None, type=str, help='specify configuration file, default None. Note: .ini file parameters can overwrite command-line parameters with the same name')


    args = parser.parse_args()
    return args

def _parse_config(config_filename):
    '''
    解析配置文件
    '''
    cp = configparser.RawConfigParser()
    cp.read(config_filename)
    config = cp.items('config')
    args = dict(config)
    for k,v in args.items():
        if k == 'n_estimators':
            args[k] = int(v)
        elif k == 'proportion':
            args[k] = float(v)
        elif k == 'batch':
            args[k] = int(v)
        elif k == 'verbose':
            args[k] = int(v)
        elif k == 'isSaveModel':
            args[k] = bool(v)
        elif k == 'isLoadModel':
            args[k] = bool(v)

    return args


def main():
    try:
        # 解析命令行参数
        args = _parse_args()
        # 获取的参数转换为字典
        args = vars(args)
        # 如果使用了 --ini 参数，则读取配置文件中的参数
        if 'config_filename' in args.keys() and args['config_filename']:
            config_args = _parse_config(args['config_filename'])
            args.update(config_args)
        # 传入参数前需要删除 config_filename 参数
        if 'config_filename' in args.keys():
            del args['config_filename']
        # 传入参数，进行异常点检测
        Outliers(**args).detect()
    except Exception as e:
        print('[ERROR] ' + str(e))
        print('[INFO] You can enter `outliers -h` to see help')


if __name__ == '__main__':
    main()