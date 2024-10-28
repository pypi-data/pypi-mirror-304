from setuptools import setup, find_packages

setup(
    name='NcatBot',
    version='1.0.3',
    author='吃点李子',
    author_email='2793415370@qq.com',
    description='基于NapCat协议端搭建的QQ机器人SDK',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    install_requires=[
        # 依赖列表
        'requests',
        'websocket-client',
        'colorama',
        'python-box',
        'pyyaml',
        
    ],
    classifiers=[
        # 项目分类
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
)