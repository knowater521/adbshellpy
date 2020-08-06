#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   adbshellpy_libunpakrom
#       By : 神郭
#  Version : 1.0
import sys,os,zipfile,urllib.request

sys.path.append(os.path.join(sys.path[0], "libromparse"))

class adbshellpyinformation():
    import platform
    p=platform.system()
    try:from adbshell_alpha import branch
    except:
        try:from adbshell import branch
        except:branch='dev'
    uselinuxpkgmanagertoinstalladb=None
    adbfile=None
    aapt=None
    conf=None

class rominformation:
    '''brotli=None
    newdat=None
    olnyimg=None
    onlyfolder=None
    ozip=None
    androidVersion=''
    flag:
    1.无效文件路径
    2.不支持格式
    3.线刷包找到
    4.卡刷包找到
    '''
    type=None #1功能性卡刷包(如opengapps) 2ROM卡刷包 3线刷包
    def __init__(self,file=''):
        '''获取ROM信息 输入的文件可以是线刷包,也可以是卡刷包'''
        if os.path.exists(file)==False:
            print('E:请选择一个正确的文件!!!')
            self.flag=1#无效文件路径
            return
        if zipfile.is_zipfile(file)==False:
            self.flag=3
            if file.find('.ozip') > -1:self.ozip=True
            if file.find('.kd') > -1:self.lgkd=True
            if file.find('.kdz') > -1:self.lgkdz=True
            if file.find('.tar.md5') > -1:self.samsumgodinfile=True
            return
        if zipfile.is_zipfile(file)==False:
            print('E:不支持的格式!!!!')
            self.flag=2
            return
        self.l=z.namelist()
        self.flag=4
        #z.close()
        if 'system.img' in self.l:
            self.olnyimg=True
        if 'system/framework/framework.jar' in self.l:
            self.onlyfolder=True
        if 'system.new.dat.br' in self.l and 'system.transfer.list' in self.l:
            self.brotil=True
        if 'system.new.dat' in self.l and 'system.transfer.list' in self.l:
            self.newdat=True
        if 'system.transfer.list' in self.l:
            z.extract('system.transfer.list')
            f = open('system.transfer.list', 'r')
            v = int(f.readline())
            f.close()
            if v == 1:
                print('Android Lollipop 5.0 检测到!\n')
                self.androidVersion='Lollipop 5.0 API 21'
            elif v == 2:
                print('Android Lollipop 5.1 检测到!\n')
                self.androidVersion='Lollipop 5.1 API 22'
            elif v == 3:
                print('Android Marshmallow 6.x 检测到!\n')
                self.androidVersion='Marshmallow 6.x API 23'
            elif v == 4:
                print('Android Nougat 7.x / Oreo 8.x 或更高版本检测到!\n')
                self.androidVersion='Nougat 7.x or higher API 24+'
        if 'payload.bin' in self.l:
            self.abflag=True
        for names in self.l:#prop获取Android版本
            if names.find('*.prop') > -1:
                try:z.extract(names)
                except:pass
                if os.path.exists('system.prop'):
                    f=open('system.prop')
                    l=[]
                    for i in f:l.append(i.strip())
                    f.close()
                    for i in l:
                        x=i.split('=')
                        if x[0]=='ro.build.version.sdk':
                            try:
                                sdk=int(x[1])
                                if sdk < 21:print('W:您处理的ROM太老旧了哦,不支持显示版本及代号,仅支持显示API版本')
                                elif sdk==21:self.androidVersion='Lollipop 5.0'
                                elif sdk ==22:self.androidVersion='Lollipop 5.1'
                                elif sdk ==23:self.androidVersion='Marshmallow 6.0'
                                elif sdk ==24:self.androidVersion='Nougat 7.0'
                                elif sdk ==25:self.androidVersion='Nougat 7.1'
                                elif sdk ==26:self.androidVersion='Oreo 8.0'
                                elif sdk ==27:self.androidVersion='Oreo 8.1'
                                elif sdk ==28:self.androidVersion='Pie 9.0'
                                elif sdk ==29:self.androidVersion='Q 10.0'
                                elif sdk ==30:self.androidVersion='R 11.0'
                                self.androidVersion=self.androidVersion+ ' API: '+x[1]
                            except:print('E:你目前处理的ROM似乎是开发者内侧版或被修改成了错误的值.')
                        
def lz4install():
    if adbshellpyinformation().p=='Linux':
        os.system('sudo apt install lz4 -y')
        os.system('sudo yum install lz4 -y')
    else:
        if os.path.exists('lz4.exe')==False:
            urllib.request.urlretrieve('https://github.wuyanzheshui.workers.dev/lz4/lz4/releases/download/v1.9.2/lz4_win32_v1_9_2.zip','lz4.zip')
            z=zipfile.ZipFile('lz4.zip')
            z.extract('lz4.exe')
            z.close()
    return
class lg_kd_kdz():
    def __init__(self,file):
        """
        GitHub Paper:https://github.com/randomstuffpaul/kdztools
        Copyright (C) 2016 Elliott Mitchell <ehem+android@m5p.com>
        Copyright (C) 2013 IOMonster (thecubed on XDA)
	    This program is free software: you can redistribute it and/or modify
	    it under the terms of the GNU General Public License as published by
	    the Free Software Foundation, either version 3 of the License, or
	    (at your option) any later version.
	    This program is distributed in the hope that it will be useful,
	    but WITHOUT ANY WARRANTY; without even the implied warranty of
	    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	    GNU General Public License for more details.
	    You should have received a copy of the GNU General Public License
	    along with this program.  If not, see <http://www.gnu.org/licenses/>.
        file 输入的文件(kdz/kd)
        """        
        if os.path.exists(file)==False:
            print('E:无效文件路径!')
            return
        
class unpackrom():
    file=''
    unpacktodir=1
    def __init__(self,file,unpacktodir=1,check=0):
        '''file:inputfile unpacktodir 0/1 0:Only run onec ;1 only to system dir check:lib 0/1'''
        self.file=file
        self.unpacktodir=unpacktodir
        if check==1:
            try:import brotli,Crypto.Cipher,binascii,stat,docopt
            except:
                print('正在安装依赖...')
                os.system('pip3 install brotli Crypto binascii stat docopt')
    def samsumg_tar(self):
        import tarfile
        tar=tarfile.open(self.file)
        tar.extractall(path='samsungrom')
        tar.close()
        lz4install()
        if adbshellpyinformation.p=='Windows':
            os.system('for %%a in (samsungrom\\*.lz4) do lz4 -d %%a')
            os.system('for %%a in (samsungrom\\*.lz4) do del /f/s/q %%a')
        else:
            os.system('find ./samsungrom -name *.lz4  |xargs lz4 -d')
            os.system('find ./samsungrom -name *.lz4  |xargs rm -rf')
    def lg_kdz(self):
        pass
    def oppo_ozip(self):
        pass
    def unzip(self):
        info=rominformation(self.file)
        if info.flag==1:return
        if info.flag==2:
            #专属格式解包
            pass
        z=zipfile.ZipFile(self.file)
        z.extractall('rom')
        z.close()
        if self.unpacktodir==0:
            print('Done! 输出的到的目录: /rom')
            return
        else:pass
    def imgunpack(self,flag=1):
        '''flag: 1mount 2unmount Linux'''
        if adbshellpyinformation.p=='Linux':
            if flag==1:
                os.system('mkdir android-system-img')
                os.system('sudo mount %s android-system-img'%self.file)
                print('Done!: 挂载镜像到文件夹 android-system-img')
            if flag==2:
                os.system('sudo umount android-system-img')
                os.system('e2fsck -p -f '+self.file)
                os.system('resize2fs -M '+self.file)
                print('Done!: 保存的镜像 '+self.file)
        if adbshellpyinformation.p=='Windows':
            url='https://github.com/AEnjoy/adbshellpy/raw/master/Imgextractor.exe'
            if os.path.exists('Imgextractor.exe')==False:
                try:urllib.request.urlretrieve(url,'Imgextractor.exe')
                except:
                    print('E:下载失败!')
                    return
            os.system('Imgextractor '+self.file)
            print('Done!')
        
    def newdatunpack(self,TRANSFER_LIST_FILE='system.transfer.list', NEW_DATA_FILE='system.new.dat', OUTPUT_IMAGE_FILE='system.img'):
        #GitHub Paper: https://github.com/xpirt/sdat2img
        #====================================================
        #          FILE: sdat2img.py
        #       AUTHORS: xpirt - luxi78 - howellzhu
        #          DATE: 2018-10-27 10:33:21 CEST
        #       Chinese: 神郭
        #====================================================
        pass

    def brotli(self,INPUT_FILE='system.new.dat.br',OUTPUT_FILE='system.new.dat',flag=1):
        import brotli as b
        if flag==1:
            f=open(INPUT_FILE)
            f=b.decompress(f.read())
            ofile=open(OUTPUT_FILE, 'wb')
            os.write(ofile,f)
            f.close()
            ofile.close()
            sys.exit()
        if flag==2:
            f=open(INPUT_FILE)
            f=b.compress(f.read())
            ofile=open(OUTPUT_FILE, 'wb')
            os.write(ofile,f)
            f.close()
            ofile.close()
            sys.exit()
        print('参数无效!')
