# NcmTranslatorScript_python

**Python脚本用于将网易云音乐（NCM）音频文件从 .ncm 格式转换。**

## 使用方法：

1. 安装依赖
```bash
pip install requests pycryptodome
```

2. 运行
### 方法一：
1. 将 `ncmTranslator.py` 脚本放置在包含要处理文件的文件夹中。
2. 执行 `./ncmTranslator.py` 运行脚本。

### 方法二：
带有绝对路径参数运行脚本：
```bash
./ncmTranslator.py {参数：指定要处理的绝对路径}
```

3. 后台运行
- `nohup ./ncmTranslator.py > ./process.log 2>&1 &`    
- 查看日志：`tail -f process.log  `  

### 注意
- 此脚本仅在Ubuntu上使用Python 3进行了测试。
- 此外，它会将专辑封面下载到与音乐文件相同的路径。
- 引用代码：[https://github.com/lianglixin/ncmdump/blob/master/folder_dump.py](https://github.com/lianglixin/ncmdump/blob/master/folder_dump.py)