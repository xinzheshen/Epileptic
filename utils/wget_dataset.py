# -*- coding: utf-8 -*-
import wget, tarfile
import urllib
import os


data_url_base = 'https://archive.physionet.org/pn6/chbmit/'
output_base = 'D:/personal/dataset/bing'
dir_name_base = "chb"
MD5SUMS = "MD5SUMS"
SHA1SUMS = "SHA1SUMS"
SHA256SUMS = "SHA256SUMS"
summary_txt = "-summary.txt"
seizures = ".seizures"

for i in range(1, 25):
    if i < 10:
        i = "0" + str(i)
    dir_name = dir_name_base + str(i)
    output_dir = os.path.join(output_base, dir_name)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    try:
        wget.download(data_url_base + dir_name + "/" + MD5SUMS, out=os.path.join(output_dir, MD5SUMS))
    except urllib.error.HTTPError:
        pass
    except Exception:
        print("fail to download " + os.path.join(output_dir, MD5SUMS))

    try:
        wget.download(data_url_base + dir_name + "/" + SHA1SUMS, out=os.path.join(output_dir, SHA1SUMS))
    except urllib.error.HTTPError:
        pass
    except Exception:
        print("fail to download " + os.path.join(output_dir, SHA1SUMS))

    try:
        wget.download(data_url_base + dir_name + "/" + SHA256SUMS, out=os.path.join(output_dir, SHA256SUMS))
    except urllib.error.HTTPError:
        pass
    except Exception:
        print("fail to download " + os.path.join(output_dir, SHA256SUMS))

    try:
        wget.download(data_url_base + dir_name + "/" + dir_name + summary_txt, out=os.path.join(output_dir, dir_name + summary_txt))
    except urllib.error.HTTPError:
        pass
    except Exception:
        print("fail to download " + os.path.join(output_dir, dir_name + summary_txt))

    for j in range(1, 100):
        if j < 10:
            j = "0" + str(j)
        file_name = dir_name + "_" + str(j) + ".edf"
        fine_name_seizures = file_name + seizures
        print("To download " + file_name)
        try:
            wget.download(data_url_base + dir_name + "/" + file_name, out=os.path.join(output_dir, file_name))
        except urllib.error.HTTPError:
            pass
        except Exception:
            print("fail to download " + os.path.join(output_dir, file_name))

        try:
            wget.download(data_url_base + dir_name + "/" + fine_name_seizures, out=os.path.join(output_dir, fine_name_seizures))
        except urllib.error.HTTPError:
            pass
        except Exception:
            print("fail to download " + os.path.join(output_dir, fine_name_seizures))


# # 提取压缩包
# tar = tarfile.open(out_fname)
# tar.extractall()
# tar.close()
# # 删除下载文件
# os.remove(out_fname)


# import unittest # 单元测试用例
# import os
# import re
# import sys
# from ftplib import FTP # 定义了FTP类，实现ftp上传和下载
#
# # 继承FTP类，对父类中retrbinary方法进行重载，实现进度条显示
# class MyFTP(FTP):
#     """
#     cmd:命令
#     callback:回调函数
#     fsize:服务器中文件总大小
#     rest:已传送文件大小
#     """
#     def retrbinary(self, cmd, callback, fsize=0, rest=0):
#         cmpsize = rest
#         self.voidcmd('TYPE I')
#         #此命令实现从指定位置开始下载,以达到续传的目的
#         conn = self.transfercmd(cmd, rest)
#         while 1:
#             if fsize:
#                 if (fsize-cmpsize) >= 1024:
#                     blocksize = 1024
#                 else:
#                     blocksize = fsize - cmpsize
#                 ret = float(cmpsize)/fsize
#                 num = ret*100
#                 # 实现同一行打印下载进度
#                 print ('下载进度: %.2f%%'%num, end='\r')
#                 data = conn.recv(blocksize)
#                 if not data:
#                     break
#                 callback(data)
#             cmpsize += blocksize
#         conn.close()
#         return self.voidresp()
#
# host = 'ftp.ncbi.nlm.nih.gov'
# port = 21
# username = ''
# password = ''
# ftp = MyFTP()
# ftp.connect(host,port)
# ftp.login(username, password)
#
# """
# RemoteFile: 要下载的文件名（服务器中）
# LocalFile: 本地文件路径
# bufsize: 服务器中文件大小
# """
# def ftp_download(LocalFile, RemoteFile, bufsize):
#     # 本地是否有此文件，来确认是否启用断点续传
#     if not os.path.exists(LocalFile):
#         with open(LocalFile, 'wb') as f:
#             ftp.retrbinary('RETR %s' % RemoteFile, f.write, bufsize)
#             f.close()
#             # ftp.set_debuglevel(0)             #关闭调试模式
#             return True
#     else:
#         p = re.compile(r'\\',re.S)
#         LocalFile = p.sub('/', LocalFile)
#         localsize = os.path.getsize(LocalFile)
#         with open(LocalFile, 'ab+') as f:
#             ftp.retrbinary('RETR %s' % RemoteFile, f.write, bufsize, localsize)
#             f.close()
#             # ftp.set_debuglevel(0)             #关闭调试模式
#             return True
#
# # 下载整个目录下的文件
# def DownLoadFileTree(LocalDir, RemoteDir):
#     print("RemoteDir:", RemoteDir)
#
#     if not os.path.exists(LocalDir):
#         os.makedirs(LocalDir)
#
#     # 打开该远程目录
#     ftp.cwd(RemoteDir)
#
#     # 获取该目录下所有文件名，列表形式
#     RemoteNames = ftp.nlst()
#     for file in RemoteNames:
#         Local = os.path.join(LocalDir, file)  # 下载到当地的全路径
#         print(ftp.nlst(file))  # [如test.txt]
#         if file.find(".") == -1:  #是否子目录 如test.txt就非子目录
#             if file.find("README") == -1:
#                 if not os.path.exists(Local):
#                     os.makedirs(Local)
#                 DownLoadFileTree(Local, file)  # 下载子目录路径
#             else:
#                 ftp.voidcmd('TYPE I') # 将传输模式改为二进制模式 ,避免提示 ftplib.error_perm: 550 SIZE not allowed in ASCII
#                 bufsize = ftp.size(file) #服务器里的文件总大小
#                 print(bufsize)
#                 ftp_download(Local, file, bufsize)
#         else:
#             ftp.voidcmd('TYPE I') # 将传输模式改为二进制模式 ,避免提示 ftplib.error_perm: 550 SIZE not allowed in ASCII
#             bufsize = ftp.size(file) #服务器里的文件总大小
#             print(bufsize)
#             ftp_download(Local, file, bufsize)
#     ftp.cwd("..")  # 返回路径最外侧
#     return
#
# class TestDownloader(unittest.TestCase):
#     def setUp(self):
#         print('------Start------')
#
#     def test_download(self):
#         file_remote = 'https://archive.physionet.org/pn6/chbmit/chb01'
#         file_local = r'D:\personal\dataset\bing\chb01\\'
#         DownLoadFileTree(file_local, file_remote)
#
#     def tearDown(self):
#         print('------Finish------')
#
# if __name__ == '__main__':
#     unittest.main()