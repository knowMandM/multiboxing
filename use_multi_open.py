# coding:utf-8

import account_manager
import multi_open
import os
import win32gui,win32con,win32api

def gbk(unicode):
    return unicode.encode('gbk')

def gbk2Utf8(gbk):
    return gbk.decode('gbk').encode('utf-8')
    
def func_del(instance):
    u'''删除记录'''
    strUsrName = raw_input(gbk('请输入要删除的用户:'))
    iCount = instance.del_record(gbk2Utf8(strUsrName))
    if iCount > 0:
        print u'删除成功！目前账号详情如下:'
    else:
        print u'未找到[%s]！目前账号详情如下:' % gbk2Utf8(strName)
    func_qryAll(instance)

def func_add(instance):
    u'''增加记录'''
    strName = raw_input(gbk('请输入用户名:'))
    strPasswd = raw_input(gbk('请输入密码:'))
    instance.add_record(instance.gen_record(gbk2Utf8(strName), gbk2Utf8(strPasswd)))
    print u'增加成功！目前账号详情如下:'
    func_qryAll(instance)
    
def func_qry(instance):
    u'''查询记录'''
    strName = raw_input(gbk('请输入要查询的用户名:'))
    listInfo = instance.qry_record(gbk2Utf8(strName))
    for record in listInfo:
        print_rec(record)
    if len(listInfo) == 0:
        print(u'未找到记录')

def func_mod(instance):
    u'''修改记录'''
    strName = raw_input(gbk('请输入要修改的用户名:'))
    strNameMod = raw_input(gbk('请输入要修改成的用户名:'))
    strPasswdMod = raw_input(gbk('请输入要修改成的密码:'))
    instance.mod_record(gbk2Utf8(strName), instance.gen_record(gbk2Utf8(strNameMod), gbk2Utf8(strPasswdMod)))
    
    print u'修改成功！修改后记录如下：',
    listInfo = instance.qry_record(gbk2Utf8(strNameMod))
    for record in listInfo:
        print_rec(record)
    
def print_rec(record):
    u'''打印一条记录'''
    print str.format('用户名:{}, 密码:{}\n', record['username'], record['password']).decode("utf-8")
    
def func_qryAll(instance):
    u'''查看所有账号'''
    print instance.tostr()
    
def func_startAll(instance):
    u'''启动所有账号'''
    multi_open.startAllProcessThread(instance.get_listAddress())
    print(u'启动完成！')
    
def func_startOne(instance):
    u'''启动一个账号'''
    os.system('cls')
    listRecord(instance)
    
    seq = 0
    while True:
        try:
            seq = int(raw_input(gbk('请输入要启动的用户序号(0~N):')))
            break
        except ValueError:
            print u'别乱输,ok?'
    
    ObjConfig = multi_open.getConfigInstance()
    multi_open.startOneProcess(seq, seq, ObjConfig, instance.get_listAddress())
    ObjConfig.saveOriInfo()
    
def chooseSeq():
    u'''选择功能号'''
    funcSeq = 0
    while True:
        try:
            funcSeq = int(raw_input(gbk('输入序号选择对应的功能:')))
            break
        except ValueError:
            print u'别乱输,ok?'
    return funcSeq

def closeWindow(instance):
    '''关闭所有模拟器'''
    while True:
        hwnd = win32gui.FindWindow('GLFW30', None)
        if hwnd > 0:
            win32api.SendMessage(hwnd, win32con.WM_CLOSE,0,0)
        else:
            break
        
def listRecord(instance):
    lst = instance.get_listAddress()
    for i in range(0, len(lst)):
        print '[%d] %s' % (i, lst[i]['username'])
        
def thank():
    print u'感谢使用！'
    
def byebye(instance):
    u'''退出'''
    thank()
    exit()

funcDict = {
    1 : func_startAll,
    2 : func_startOne,
    3 : func_qryAll,
    4 : func_qry,
    5 : func_mod,
    6 : func_add,
    7 : func_del,
    8 : closeWindow,
    9 : byebye
}

def printFunctions():
    u'''打印所有功能'''
    for key in funcDict.keys():
        print ("%d: %s" % (key, funcDict[key].__doc__)).decode('utf-8')
    

if __name__ == "__main__"    :
    tip = u'''\
#============================================================#
#                   多开V1.0 by chenej                       #
#                   Created on 2017.12.14                    #
#============================================================#
'''
    dumpFile = '''D:\Account.dmp'''
    obj = account_manager.AddressRecord(dumpFile)

    while True:
        print tip
        printFunctions()
        funcSeq = chooseSeq()
        funcDict[funcSeq](obj)
        
        print
        raw_input(gbk('按Enter继续...'))
        os.system('cls')
    
    thank()

