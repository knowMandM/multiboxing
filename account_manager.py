# coding:utf-8
# filename:address_book.py

import cPickle
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

u'''\
    这个是一账户管理类
    实现添加删除等功能
'''

class AddressRecord:
    u'''通讯录类'''
    
    def __init__(self, strFilePath):
        u'''初始化，读取指定的账号文件'''
        if self.read_record(strFilePath) != True:
            self.listAddresRecord = []
        self.dumpFileName = strFilePath
    
    def add_record(self, dictInfo):
        u'''增加一条记录'''
        self.listAddresRecord.append(dictInfo)
        self.save_record();

    def del_record(self, name):
        u'''删除指定名字的记录'''
        lenBeforDel = len(self.listAddresRecord)
        self.listAddresRecord = [i for i in self.listAddresRecord if i['username'] != name]
        lenAfterDel = len(self.listAddresRecord)
        self.save_record()
        return lenBeforDel - lenAfterDel
        
    def mod_record(self, name, dictInfo):
        u'''修改记录'''
        for i in range(0, len(self.listAddresRecord)):
            if self.listAddresRecord[i]['username'] == name:
                self.listAddresRecord[i] = dictInfo
        self.save_record()

    def qry_record(self, name):
        u'''查询记录'''
        listRet = []
        for i in range(0, len(self.listAddresRecord)):
            if self.listAddresRecord[i]['username'] == name:
                listRet.append(self.listAddresRecord[i])
                
        return listRet

    def save_record(self):
        u'''保存记录'''
        f = file(self.dumpFileName, 'w')
        cPickle.dump(self.listAddresRecord, f)

    def read_record(self, strFilePath):
        u'''读取记录'''
        if os.path.exists(strFilePath):
            f = file(strFilePath)
            self.listAddresRecord = cPickle.load(f)
            return True
        return False
    
    def gen_record(self, username, password):
        u'''生成一对用户密码'''
        dictInfo = {'username':username, 'password':password}
        return dictInfo
    
    def get_listAddress(self):
        u'''返回通讯录数据'''
        return self.listAddresRecord
    
    def tostr(self):
        retStr = ""
        for record in self.listAddresRecord:
            retStr = retStr + str.format('用户名:{}, 密码:{}\n', record['username'], record['password'])

        return retStr.decode("utf-8")
        
if __name__ == "__main__":
    dumpFile = '''./AdressRecord.data'''
    obj = AddressRecord(dumpFile)
    print obj.tostr()
