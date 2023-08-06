from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='package_wish',  # 包名
    version='1.0.0',
    packages=find_packages(),
    url='https://blog.csdn.net/qq_40672115/article/details/127012332?spm=1001.2014.3001.5502',
    license='MIT',
    author='Z',
    author_email='1941981477@qq.com',
    description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
        'numpy',
        'opencv-python'
    ]
)