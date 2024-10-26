# 导入子包和模块到包的顶层命名空间
from onetouch.one2three import *
from onetouch.superprint import *


__description__ = "一款基于PyTorch、Pandas、Scikit-learn、Matplotlib、NumPy等库的简单便捷的Python自动化工具包，提供一键数据清洗、模型训练、模型评估、自动超参数调优和预测等功能。"
__version__ = '0.1.23'
__author__ = '17fine'
__email__ = '2756601885@qq.com'
__license__ = 'MIT'
__shortname__ = 'ot'

# ANSI 转义码
RED = '\033[91m'  # 红色
GREEN = '\033[92m'   # 绿色
YELLOW = '\033[93m'  # 黄色
RESET = '\033[0m'  # 重置为默认颜色
