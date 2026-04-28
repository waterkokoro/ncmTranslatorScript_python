<div align="center">

# 🎵 ncmTranslatorScript_python

网易云音乐 `.ncm` 加密格式批量转换工具

将网易云音乐专属的 `.ncm` 加密文件解密转换为标准音频格式（MP3 / FLAC），并自动下载专辑封面。

</div>

---

## ✨ 功能特性

- 🔓 解密 `.ncm` 文件，转换为原始音频格式（MP3 / FLAC / WAV / APE）
- 🖼️ 自动下载专辑封面图片，保存至音乐文件同目录
- 📁 支持文件夹递归批量处理
- 🚫 自动跳过已转换的同名文件，避免重复处理
- 🖥️ 支持后台运行，适合大批量任务

## 📋 依赖环境

- **Python** 3.x
- **PyCryptodome**（提供 AES 解密）
- **requests**

安装依赖：

```bash
pip install pycryptodome requests
```

## 🚀 使用方法

### 方式一：处理脚本所在目录

将 `ncmTranslator.py` 放到包含 `.ncm` 文件的文件夹下，然后执行：

```bash
python3 ncmTranslator.py
```

### 方式二：指定目标路径

```bash
python3 ncmTranslator.py /path/to/your/ncm/files
```

### 后台运行

适合大量文件处理，避免终端关闭导致中断：

```bash
nohup python3 ncmTranslator.py /path/to/ncm > process.log 2>&1 &
```

查看处理日志：

```bash
tail -f process.log
```

## 📂 转换示例

```
转换前                        转换后
├── 晴天.ncm                  ├── 晴天.mp3
                              ├── 晴天.jpg   (专辑封面)
```

## 🙏 致谢

- 核心解密逻辑参考自 [ncmdump](https://github.com/lianglixin/ncmdump/blob/master/folder_dump.py)

## 📄 License

MIT License

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=waterkokoro/ncmTranslatorScript_python&type=Date)](https://star-history.com/#waterkokoro/ncmTranslatorScript_python&Date)
