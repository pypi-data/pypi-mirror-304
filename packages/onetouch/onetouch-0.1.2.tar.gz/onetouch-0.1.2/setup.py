from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

with open('requirements.txt', 'r', encoding='utf-8') as file:
    requirements = file.read().splitlines()

setup(
    name='onetouch',  # 包名，应与你要发布的包名一致
    version='0.1.2',  # 包的版本号
    author='17fine',  # 作者名字
    author_email='2756601885@qq.com',  # 作者的电子邮件
    description='a package designed to streamline data processing, model training, and evaluation with minimal code.',  # 简短描述
    long_description=long_description,  # 长描述，通常是README文件的内容
    long_description_content_type='text/markdown',  # 长描述的内容类型，这里使用Markdown
    url='https://gitee.com/SunnyB0y/onetouch',  # 项目的主页URL
    packages=['onetouch'],  # 自动查找并列出所有包
    classifiers=[  # 分类信息，有助于PyPI用户找到你的包
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 指定支持的Python版本
    install_requires=requirements,
    extras_require={  # 可选依赖
        'dev': [
            requirements
        ]
    }
)
