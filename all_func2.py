# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 18:50:25 2014

@author: Administrator
"""

import os
import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt


def get_files(file_type):
    """
       读取当前目录中所有的 file_type 类型文件,返回一个由文件名组成的list
       参数为所需文件类型 如：‘xls’
    """
    a_walk = list(os.walk(os.getcwd()))
    a_files = []
    for i in a_walk:
        for j in i[2]:
            a_files.append(i[0] + '\\' + j)        
    obj = [i for i in a_files if os.path.splitext(i)[1] == '.' + file_type]            
    return obj
    
def xls_to_csv(xlsfile, filename):
    """
       将一个list对象给定的所以xls文件，保存到一个csv文件中
       参数为xls文件名组成的list，csv文件的存储文件名
    """
    pd_file = [pd.ExcelFile(name).parse('data') for name in xlsfile]
    pd_cat = pd.concat(pd_file)
    pd_cat.to_csv(filename)
    
def csv_to_list(filename):
    """
       读取一个csv文件，生成一个list对象
       filename：csv文件名
    """
    infile = open(filename, 'r')
    e = []
    for i in infile:
        a = i.strip('\n')
        b = a.split(sep = ',')
        e.append(b)
    infile.close()
    return e
    
def save_list(list_name,filename):
    """
       将一个list对象，保存到一个 CSV 文件中
       list_name：需要保持的list变量名
       filename：csv文件名
    """
    outfile = open(filename, 'w')
    for row in list_name:
        for column in row:
            outfile.write(str(column) + ',')
        outfile.write('\n')
    outfile.close()
    
def append_parameters(para_file, data_file, filename):
    """
       将参数附加到每个对应数据项之后
       para_file：csv格式的参数存储文件
       data_file：csv格式的数据存储文件
       filename：保存结果的csv文件
    """
    para = csv_to_list(para_file)
    data = csv_to_list(data_file)
    for i in data:
        for j in para:
            if i[1] == j[0] and i[2] == j[1]:
                i.extend(j)
    data2 = [[row[12], row[1], row[2], row[8], row[4],  row[5],\
            row[19], row[14], row[15], row[16], row[17], row[20]]\
            for row in data if len(row) == 21]         
    save_list(data2, filename)
    return data2 

def filtrate_data(data):
    """
       将数据中的无效行，顾虑掉
       data:存储数据的list"""
    data2 = [row for row in data if row[4] != '0' and row[5] != '---']
    save_list(data2, 'filtrated_data.csv')
    return data2

def sort_data(data, filename=None):
    """
       将data中的数据按时间排序
       data：需排序数据
       filename：排序后，数据存储文件
    """
    data2 = data[1:]
    d = {}
    for row in data2:
        d[row[3]] = row
    keys = list(d.keys())
    data3 = [d[i] for i in sorted(keys)]
    data3.insert(0, data[0])
    if filename != None:
        save_list(data3, filename)
    return data3

    
    
def g(row):
    """计算一条数据的结果"""
    r = row
    ans =  float(r[7])*( float(r[4])**2 -  float(r[9])**2) - \
    float(r[8])*( float(r[5]) - float(r[10]))
    return ans
    
def get_target(data, target, day):
    """
       从data中提取 target 项
       data： 数据存储文件,list
       target：所选数据项
    """
    t = [row for row in data if row[0] == target and row[3][6:8] == day]
    return t
    
def plot_target(data,target,day,directory=None):
    """
       输入传感器编号，画出相应的时间序列图
       data：数据存储对象，list
       target: 传感器编号，str 例如“T1-1”
       directory：图片存储位置
    """
    t = get_target(data,target,day)
    x = [dt.strptime(row[3][:-4], '%y-%m-%d %H:%M:%S') for row in t]
    y = [float(row[-1]) for row in t]
    
    fig = plt.figure(figsize = (5, 1), dpi = 300)
    ax = fig.add_axes([0.07, 0.1, 0.84, 0.80])
    ax.plot(x, y)
    ax.grid(color='g', linestyle='--')
    
    string = '%s' % target
    fig.text(0.92, 0.8,string, transform = ax.transAxes)
    fig.text(0.01, 0.5, 'Unit:\n(kPa)')
    if directory != None:
        target_dir = directory + '\\' + 'target'
        fig.savefig(target_dir, dpi=300)
    
    plt.show()
    plt.savefig(target)
    plt.close()
    
def make_directory(dir_name):
    cwd = os.getcwd()
    directory = cwd + '\\' + dir_name
    while os.path.isdir(directory):
        directory = directory + '+'
    os.mkdir(directory)
    return directory
    
def get_keys(data):
    d = {}
    for i in data:
        d[i] = d.get(i, 0) + 1
    L = list(d.keys())
    return L
    

if __name__ == '__main__':
    directory = make_directory('result')
    
    xls = get_files('xls')
    print('The number of xls file is %d' % len(xls))
    
    name1 = directory + '\\' + 'test.csv' #原始数据
    name2 = directory + '\\' + 'data_with_para.csv'#
    name3 = directory + '\\' + 'final_result.csv'
    
    xls_to_csv(xls, name1)
    data = append_parameters('parameters.csv', name1, name2)
    data2 = filtrate_data(data)
    data2 = sort_data(data2)
    res = [g(row) for row in data2[1:]]
    for i in range(len(res)):
        data2[i+1].append(res[i])
    save_list(data2, name3)
    
    date = [i[3] for i in data2]
    year = [i[0:2] for i in date]
    month = [i[] for i in date]
    



    