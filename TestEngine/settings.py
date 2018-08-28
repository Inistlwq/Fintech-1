#coding:utf-8
import ConfigParser
import os
import sys

'''
settings of DB module
'''
class ConfigModule(object):

    def __init__(self):
        #将项目目录添加到编译器path中
        sys.path.append(self.project_path)

    @property
    def project_path(self):
        return os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

if __name__ =='__main__':
    c = ConfigModule()
    print c.settings