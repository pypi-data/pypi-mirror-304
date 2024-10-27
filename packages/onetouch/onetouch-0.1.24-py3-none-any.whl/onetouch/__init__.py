# 导入子包和模块到包的顶层命名空间
from onetouch.models import GPT as GPT, config
from onetouch.models import *
from onetouch.one2three import *
from onetouch.tools.superprint import *
from onetouch.tools.readeverything import *
from onetouch.models.GPT import *

__all__ = [
    'prints', 'printc', 'one2three', 'One2Three', 'read_file', 'GPTModel', 'generate', 'GPT', 'config'
]


__description__ = ("一款基于PyTorch、Pandas、Scikit-learn、Matplotlib、NumPy等库的简单便捷的"
                   "Python自动化工具包，提供一键数据清洗、模型训练、模型评估、自动超参数调优和预测等功能。")
__version__ = '0.1.24'
__author__ = '17fine'
__email__ = '2756601885@qq.com'
__license__ = 'MIT'
__shortname__ = 'ot'
