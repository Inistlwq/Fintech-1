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

        #检查设置文件
        self._settings_path = os.path.join(self.project_path,'settings.ini')
        self._config = ConfigParser.ConfigParser()

        self._settings = {}
        if os.path.isfile(self._settings_path):
            self._config.read(self._settings_path)
            for section in self._config.sections():
                self._settings[section] = {}
                for item in self._config.items(section):
                    self._settings[section][item[0]] = item[1]

        else:
            with open(self._settings_path,'w') as fp:
                #初始化配置文件

                '''数据库配置'''
                self._config.add_section('DB')
                default_DB_path = os.path.join(self.project_path,'tushare_pro_database.sqlite3')
                self._config.set('DB','DB_path',default_DB_path)
                self._config.set('DB', 'ts_token', '9aba5c3c126c0e9cb91691daf09cc3802f394dba91a576ad692b2a9b')
                self._config.write(fp)

    @property
    def project_path(self):
        return os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

    @property
    def settings(self):
        return self._settings

if __name__ =='__main__':
    c = ConfigModule()
    print c.settings