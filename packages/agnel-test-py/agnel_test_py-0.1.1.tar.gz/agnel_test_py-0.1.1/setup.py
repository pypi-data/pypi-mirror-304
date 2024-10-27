# setup.py

from setuptools import setup, find_packages

setup(
    name='agnel_test_py',
    version='0.1.1',
    packages=find_packages(),
    description='A simple example package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my-package',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    install_requires=[
        # 依赖列表
    ],
)