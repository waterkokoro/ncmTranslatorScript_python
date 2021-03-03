#!/usr/bin/python3
# Modifier: Liang Lixin
# Folder dump version by LiangLixin
import binascii
import struct
import base64
import json
import os
import logging
import urllib 
import requests
import time

from Crypto.Cipher import AES

music_suffix_list = ['mp3', 'wav', 'ape', 'flac', 'MP3', 'WAV', 'APE', 'FLAC']
def dump(file_path, file_name_no_suffix):
    core_key = binascii.a2b_hex("687A4852416D736F356B496E62617857")
    meta_key = binascii.a2b_hex("2331346C6A6B5F215C5D2630553C2728")
    unpad = lambda s : s[0:-(s[-1] if type(s[-1]) == int else ord(s[-1]))]
    f = open(file_path,'rb')
    header = f.read(8)
    assert binascii.b2a_hex(header) == b'4354454e4644414d'
    f.seek(2, 1)
    key_length = f.read(4)
    key_length = struct.unpack('<I', bytes(key_length))[0]
    key_data = f.read(key_length)
    key_data_array = bytearray(key_data)
    for i in range (0,len(key_data_array)): key_data_array[i] ^= 0x64
    key_data = bytes(key_data_array)
    cryptor = AES.new(core_key, AES.MODE_ECB)
    key_data = unpad(cryptor.decrypt(key_data))[17:]
    key_length = len(key_data)
    key_data = bytearray(key_data)
    key_box = bytearray(range(256))
    c = 0
    last_byte = 0
    key_offset = 0
    for i in range(256):
        swap = key_box[i]
        c = (swap + last_byte + key_data[key_offset]) & 0xff
        key_offset += 1
        if key_offset >= key_length: key_offset = 0
        key_box[i] = key_box[c]
        key_box[c] = swap
        last_byte = c
    meta_length = f.read(4)
    meta_length = struct.unpack('<I', bytes(meta_length))[0]
    meta_data = f.read(meta_length)
    meta_data_array = bytearray(meta_data)
    for i in range(0,len(meta_data_array)): meta_data_array[i] ^= 0x63
    meta_data = bytes(meta_data_array)
    meta_data = base64.b64decode(meta_data[22:])
    cryptor = AES.new(meta_key, AES.MODE_ECB)
    meta_data = unpad(cryptor.decrypt(meta_data)).decode('utf-8')[6:]
    meta_data = json.loads(meta_data)
    crc32 = f.read(4)
    crc32 = struct.unpack('<I', bytes(crc32))[0]
    f.seek(5, 1)
    image_size = f.read(4)
    image_size = struct.unpack('<I', bytes(image_size))[0]
    image_data = f.read(image_size)
    file_name = file_name_no_suffix + '.' + meta_data['format']

    ## delete
    # try:
    #     os.remove(os.path.join(os.path.split(file_path)[0], meta_data['musicName'] + '.' + meta_data['format']))
    #     print('删除文件 :' + os.path.join(os.path.split(file_path)[0], meta_data['musicName'] + '.' + meta_data['format']))
    #     ## delete 
    # except Exception as e:
    #     print('删除失败', e)
    

    m = open(os.path.join(os.path.split(file_path)[0],file_name),'wb')
    chunk = bytearray()
    while True:
        chunk = bytearray(f.read(0x8000))
        chunk_length = len(chunk)
        if not chunk:
            break
        for i in range(1,chunk_length+1):
            j = i & 0xff;
            chunk[i-1] ^= key_box[(key_box[j] + key_box[(key_box[j] + j) & 0xff]) & 0xff]
        m.write(chunk)
    m.close()
    f.close()
    try:
        urllib.request.urlretrieve(meta_data['albumPic'], os.path.join(os.path.split(file_path)[0], file_name_no_suffix) + '.jpg');
    except Exception as e:
        print('下载专辑图片出错', e)

def file_extension(path):
    return os.path.splitext(path)[1]

def file_no_extension(path):
    return os.path.splitext(path)[0]

def file_exist(file_name, file_list, file_list_path):
    for file in file_list:
        if (os.path.isdir(os.path.join(file_list_path, file))):
            # print('######### 文件夹, 跳过')
            continue
        for suffix in music_suffix_list:
            if (file_no_extension(file_name) + "." + suffix) == file:
                return True;
    return False;

def recursion(file_name, root_dir, file_list):
    # print('root_dir: ' + root_dir)
    # print('file_name: ' + file_name)
    full_file = os.path.join(root_dir, file_name)
    if os.path.isfile(full_file):
        print('>>>>>>>>>>>>>>>> 当前文件: ' + full_file)
        if file_extension(full_file) == ".ncm":
            # 校验文件存在同名
            if file_exist(file_name, file_list, root_dir):
                print('>>>>>>>>>>>>>>> 同名文件跳过: ' + full_file)
                return
            try:
                print('>>>>>>>>>>>>>>> 开始转码文件: ' + full_file)
                dump(full_file, file_no_extension(file_name));
                print('>>>>>>>>>>>>>>> 转码文件成功: ' + full_file)
            except Exception as err:
                print('转码文件失败: ' + full_file + ' error: ' + err)
        else:
            print('>>>>>>>>>>>>>>> 非ncm文件, 跳过')
    elif os.path.isdir(full_file):
        print('>>>>>>>>>>>>>>> 处理当前文件夹内容: ' + full_file)
        list = os.listdir(full_file)
        for i in range(0, len(list)):
            recursion(list[i], full_file, list)
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        rootdir = sys.argv[1]; #如果有输入路径参数，取当前路径参数
    else:
        # 没写路径默认走当前文件夹
        rootdir = os.path.split(os.path.realpath(__file__))[0];
    print('>>>>>>>>>>>>>>> 初始路径层级: ' + rootdir)
    list = os.listdir(rootdir) # Get all files in folder.is
    for i in range(0,len(list)):
        try:
            recursion(list[i], rootdir, list)
        except Exception as e:
            print('递归处理出现错误');
            logging.exception(e)
        finally:
            pass

    print('全部文件处理完成 ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()));
