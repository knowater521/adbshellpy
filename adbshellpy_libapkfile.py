#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   adbshellpy_libapkfile.py
#       By : 神郭
#  Version : 0.6.2 Stable
#  要关联apk文件 输入命令
#  adbshellpy_libapkfile.py -relatedapk
#  release
# Do not try to import this file in Python! 
import sys,os
import zipfile as zip
os.chdir(os.getcwd())
try:from adbshell import errexit,update,checkinternet,clear,adbcommand,install,changes,github,version,builddate,p,adbfile,conf   
except:from adbshell_alpha import errexit,update,checkinternet,clear,adbcommand,install,changes,github,version,builddate,p,adbfile,conf
class adbshellpyinformation:
    global conf
    p=None
    branch=None
    uselinuxpkgmanagertoinstalladb=None
    adbfile=None
    try:
        aapt=conf.get('adbshell', 'aaptfile')
    except:
        aapt=r'build-tools\android-10\aapt.exe' #windows
        #aapt=r'build-tools/android-10/aapt' #Linux
        #从旧版升级
    Permissionshow=True
class apk:
    pakname=None
    permissions=None
    minsdk=None
    targetsdk=None
    appname=None
    apkinstall= False #开发计划2
    apkfile=[]#开发计划2

aapt=adbshellpyinformation.aapt
Permissionshow=adbshellpyinformation.Permissionshow

def permissions(file):
    global aapt
    r=os.popen(aapt+' d permissions "'+file+'"')
    t=r.read()
    r.close()
    return t
    
def installaapt():
    global p ,conf ,aapt
    import urllib.request
    if p=='Linux':
        url='https://dl.google.com/android/repository/build-tools_r29.0.6-linux.zip'
        urllib.request.urlretrieve(url,'build-tools.zip') 
        z=zip.ZipFile('build-tools.zip','r')
        z.extractall(path='build-tools')
        z.close()
        aapt=r'build-tools/android-10/aapt'
        conf.set("adbshell", "aaptfile", aapt)
        conf.write(open("adbshell.ini", "w"))
    if p=='Windows':
        url='https://dl.google.com/android/repository/build-tools_r29.0.6-windows.zip'
        urllib.request.urlretrieve(url,'build-tools.zip')
        z=zip.ZipFile('build-tools.zip','r')
        z.extractall(path='build-tools')
        z.close()
        aapt=r'build-tools\android-10\aapt.exe'
        conf.set("adbshell", "aaptfile", aapt)
        conf.write(open("adbshell.ini", "w"))
    os.remove('build-tools.zip')
def apkinstallmode(install=False,file=[]):#开发计划2
    global p ,conf ,aapt ,Permissionshow ,adbfile
    if install==True:#apk安装模式
        '''
        if os.path.exists(str(aapt))==False:
            installaapt()
        '''
        if os.path.exists('build-tools')==False or os.path.exists(aapt)==False:
            installaapt()
        #开始apk安装
        print('您将要安装Android应用程序,个数:'+str(len(file))+' 您确定要安装吗?y/n')
        a=input('>>>')
        if a=='n' or a=='N':
            return
        for i in range(len(file)):
            nowfile=file[i]
            print('正在安装的程序:'+str(i)+'/'+str(len(file))+' 文件:'+nowfile)
            if Permissionshow:
                print(' 程序权限:'+permissions(nowfile))
            adbcommand().install(nowfile)
        print('安装完成!')
        sys.exit(0)
    if install==False:
        print('没有安装包需要安装.')
        input('按任意键继续')
        sys.exit(0)
def ParseArguments(args): #解析参数
    apkfile=[]
    apkinstall=False
    if len(args)==0:
        print('''adbshellpy_libapkfile.py [apkfile(s)]
        [apkfile(s)]       欲安装的apk文件 支持多个文件
        ''')
        return apkfile,apkinstall
    if os.path.exists(args[0]):#-1
        apkinstall=True
        for i in range(len(args)):
            if os.path.exists(args[i]):
                apkfile.append(args[i])
            else:
                break
        #apk file End
    return apkfile,apkinstall
def relatedApkfile():
    global p
    if p=='Windows':
        print('W:您可能需要管理员权限运行!')
        os.system(r'reg delete "HKEY_CLASSES_ROOT\.apk" /f')
        os.system(r'reg delete "HKEY_CURRENT_USER\SOFTWARE\Classes\.apk" /f')
        os.system(r'reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Classes\.apk" /f')
        os.system(r'reg delete "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.apk" /f')
        os.system(r'')
        os.system(r'reg add "HKCR\.apk" /f /ve /t REG_SZ /d "adbshellpy.apk"')
        os.system(r'reg add "HKCR\adbshellpy.apk" /f /ve /t REG_SZ /d "Android Application Package"')
        os.system('reg add "HKCR\\adbshellpy.apk\\DefaultIcon" /f /ve /t REG_SZ /d "'+os.getcwd()+'\\apk.ico\\"')
        os.system(r'reg add "HKCR\adbshellpy.apk\shell" /f /ve /t REG_SZ /d "open"')
        os.system(r'reg add "HKCR\adbshellpy.apk\shell\open" /f /ve /t REG_SZ /d "查看或安装"')
        os.system('reg add "HKCR\\adbshellpy.apk\\shell\\open" /f /v Icon /t REG_SZ /d "'+os.getcwd()+'\\apk.ico\\"')
        os.system('reg add "HKCR\\adbshellpy.apk\\shell\\open\\command" /f /ve /t REG_SZ /d ""py.exe" "'+os.getcwd()+'\\adbshellpy_libapkfile.py" "%%1\""')
    else:
        errexit(7)
        return
    import platform
    if platform.machine()=='AMD64':
        net_dir=os.environ.get('windir')+'\\Microsoft.NET\\Framework64\\v4.0.30319\\regasm.exe'
    else:
        net_dir=os.environ.get('windir')+'\\Microsoft.NET\\Framework\\v4.0.30319\\regasm.exe'
    if os.path.exists(net_dir):
        if os.path.exists('apkshellext.dll'):
            print('显示apk原本图标...')
            os.system('"'+net_dir+'" /codebase apkshellext.dll')
        else:
            print('W:文件 apkshellext.dll 缺失,apk图标将不会关联')
    else:
        print('E:Microsoft.NET v4.0.30319 or newer is required, but it isnot installed !')
        return
def main(args):
    apkfile,apkinstall=ParseArguments(args)
    apk.apkfile=apkfile
    apk.apkinstall=apkinstall
    apkinstallmode(apk.apkinstall,apk.apkfile)
def mainex(list):
    apkinstallmode(True,list) 
if __name__ == '__main__':
    try:
        if str(sys.argv[1])=='-relatedapk':
            relatedApkfile()
            print('Done!')
            sys.exit(0)
    except:pass
    main(sys.argv[1:])