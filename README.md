## outliers
> 异常点检测的命令行版本

## 依赖
```
wheel>=0.32.3
numpy>=1.14.5
six>=1.5
python-dateutil>=2
pytz>=2011k
pandas>=0.22.0
SciPy>= 0.13.3
scikit-learn>=0.19.2
```

Note: 离线安装的话，whl安装包可在 https://pypi.org 中搜索下载

## 安装
```
chmod +x install.sh
./install.sh
```

## 用法
```
>>> python outliers.py -h
usage: outliers.py [-h] [-i INPUT_FILENAME] [-o OUTPUT_FILENAME]
                   [-n N_ESTIMATORS] [-p PROPORTION] [-b BATCH] [-v VERBOSE]
                   [-s] [-l] [-m MODELNAME] [--ini CONFIG_FILENAME]

A outliers detect tool.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILENAME, --input INPUT_FILENAME
                        specify the input file, default `data.csv`
  -o OUTPUT_FILENAME, --output OUTPUT_FILENAME
                        specify the output file, default `outliers_result.csv`
  -p PROPORTION, --proportion PROPORTION
                        the proportion of outliers in the data set, default 0.001
  -b BATCH, --batch BATCH
                        batch size for predicting, default 256
  -n N_ESTIMATORS, --n_estimators N_ESTIMATORS
                        the number of base estimators in the ensemble, default 100
  -s, --isSaveModel     whether to save the model after training.
                        False (default) => train and predict, not save model. 
                        True => only train, then save the model
  -l, --isLoadModel     whether to load the local model for prediction. 
                        False (default) => train and predict. 
                        True => load local model and predict
  -m MODELNAME, --model MODELNAME
                        specify the saved model name, default `IsolationForest.model`
  --ini CONFIG_FILENAME
                        specify configuration file, default None. 
                        Note: .ini file parameters can overwrite command-line parameters with the same name
```

## 样例
#### 不指定任何参数
```
>>> python outliers.py
Reading `data.csv`...
Data preprocessing...
Model training...
Outliers predicting...
Writing `outliers_result.csv`...
```

#### 指定输入输出文件
```
>>> python outliers.py -i test_input.csv -o test_result.csv
Reading `test_input.csv`...
Data preprocessing...
Model training...
Outliers predicting...
Writing `test_result.csv`...
```

#### 训练参数
```
>>> python outliers.py -n 200 -p 0.1 -b 128 -v 1
Reading `data.csv`...
Data preprocessing...
Model training...
[Parallel(n_jobs=4)]: Done   2 out of   4 | elapsed:    2.0s remaining:    2.0s
[Parallel(n_jobs=4)]: Done   4 out of   4 | elapsed:    2.0s finished
Outliers predicting...
Writing `outliers_result.csv`...
```

#### 模型保存/加载控制
```
# 只训练并保存模型，不预测。默认保存的模型名为 `IsolationForest.model`
>>> python outliers.py -s
Reading `data.csv`...
Data preprocessing...
Model training...
Saving model to `IsolationForest.model`...
Don't predict.

# 只训练并保存模型，不预测。指定要保存的模型名
>>> python outliers.py -s -m test.mod
Reading `data.csv`...
Data preprocessing...
Model training...
Saving model to `test.mod`...
Don't predict.

# 加载本地模型，然后预测，指定加载的模型
>>> python outliers.py -l -m test.mod
Reading `data.csv`...
Data preprocessing...
Loading model from `test.mod`...
Outliers predicting...
Writing `outliers_result.csv`...

# 训练且预测，并保存模型到本地，指定模型名称
>>> python outliers.py -sl -m test.mod
Reading `data.csv`...
Data preprocessing...
Model training...
Saving model to `test.mod`...
Outliers predicting...
Writing `outliers_result.csv`...
```

#### 使用配置文件
配置文件样例 config.ini
```
[config]
proportion = 0.01
verbose = 1
isSaveModel = True
modelname = test.model
```
运行
```
>>> python outliers.py --ini config.ini
Reading `data.csv`...
Data preprocessing...
Model training...
[Parallel(n_jobs=4)]: Done   2 out of   4 | elapsed:    2.1s remaining:    2.1s
[Parallel(n_jobs=4)]: Done   4 out of   4 | elapsed:    2.2s finished
Saving model to `test.model`...
Don't predict.
```

## 参考资料
* Save and Load Machine Learning Models in Python with scikit-learn(孤立森林模型的保存和加载)  
https://machinelearningmastery.com/save-load-machine-learning-models-python-scikit-learn/

#### 使用 argparse 解析命令行参数
* argparse — Parser for command-line options, arguments and sub-commands(argparse 官方文档)  
https://docs.python.org/3/library/argparse.html

* argparse - 命令行选项与参数解析（译）(argparse 中文教程)  
https://www.cnblogs.com/lovemyspring/p/3214598.html

* python学习之argparse模块  
https://zhuanlan.zhihu.com/p/28871131

#### 使用 python setup.py 打包
* python的构建工具setup.py  
https://www.cnblogs.com/maociping/p/6633948.html

* python的setup问题(比较详细)  
https://blog.csdn.net/langb2014/article/details/53114341

* 使用 Setup 将Python 代码 打包  
http://www.cnblogs.com/yunfeiqi/p/6844771.html

* Python 打包，entry_points的使用  
https://blog.csdn.net/llsmingyi/article/details/78691287

* python setup.py uninstall - stackoverflow  
https://stackoverflow.com/questions/1550226/python-setup-py-uninstall

