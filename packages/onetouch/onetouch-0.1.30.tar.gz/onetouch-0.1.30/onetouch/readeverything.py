import os

import pandas as pd

file_dict = {
    'Image': ['jpg', 'png', 'gif', 'webp'],
    'Video': ['rmvb', 'mp4', 'avi', 'mkv', 'flv'],
    "Audio": ['cd', 'wave', 'aiff', 'mpeg', 'mp3', 'mpeg-4'],
    'DocFiles': ['xls', 'xlsx', 'csv', 'doc', 'docx', 'ppt', 'pptx', 'pdf', 'txt'],
    'CompressFiles': ['7z', 'ace', 'bz', 'jar', 'rar', 'tar', 'zip', 'gz'],
    'CommonFiles': ['json', 'xml', 'md'],
    'ProgramFiles': ['py', 'java', 'html', 'sql', 'r', 'css', 'cpp', 'c', 'sas', 'js', 'go', 'ipynb'],
    'ExecutableFiles': ['exe', 'bat', 'lnk', 'sys', 'com'],
    'FontFiles': ['eot', 'otf', 'fon', 'font', 'ttf', 'ttc', 'woff', 'woff2']
}


def read_file(FilePath, OutputPath):
    # 获取文件的扩展名
    filename, file_extension = os.path.splitext(FilePath)
    file_extension = file_extension.lower()  # 确保扩展名是小写的

    # # 根据文件扩展名调用不同的处理函数
    # if file_extension == '.txt':
    #     return process_txt(file_path)
    # elif file_extension == '.csv':
    #     return process_csv(file_path)
    # elif file_extension == '.json':
    #     return process_json(file_path)
    # else:
    #     raise ValueError(f"Unsupported file format: {file_extension}")
