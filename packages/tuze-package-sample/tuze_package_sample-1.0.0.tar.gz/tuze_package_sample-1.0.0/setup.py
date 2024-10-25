from setuptools import find_packages, setup

setup(
    name='tuze_package_sample',  # 包的名字
    version='1.0.0',  # 包的版本
    author='tuze',  # 作者名字
    author_email='sharkshore@163.com',  # 作者邮箱
    description='A useful tool package',  # 简短描述
    long_description=open('README.md').read(),  # 从README中读取完整描述
    long_description_content_type='text/markdown',  # README文件类型
    url='https://github.com/sharkshore/python-base-sample',  # 项目主页URL
    packages=find_packages(),  # 自动找到所有的包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 指定 Python 版本要求
    install_requires=[        # 列出项目依赖的第三方包
        'requests',
        'colorama',
    ],
)
