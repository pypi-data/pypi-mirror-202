import os
import shutil

import setuptools

package_root = os.path.abspath(os.path.dirname(__file__))

name = 'dashscope'

description = 'dashscope client sdk library'


def get_version():
    version_file = os.path.join(package_root, name, 'version.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


def get_dependencies(fname='requirements.txt'):
    with open(fname, 'r') as f:
        dependencies = f.readlines()
        return dependencies


url = 'https://dashscope.aliyun.com/'


def readme():
    with open(os.path.join(package_root, 'README.md'), encoding='utf-8') as f:
        content = f.read()
    return content


def pack_resource():
    # pack resource such as configs and tools
    root_dir = 'package/'
    if os.path.isdir(root_dir):
        shutil.rmtree(root_dir)
    os.makedirs(root_dir)

    proj_dir = root_dir + 'dashscope/'
    shutil.copytree('./dashscope', proj_dir)
    shutil.copy('./requirements.txt', 'package/requirements.txt')
    shutil.copy('./README.md', 'package/README.md')


setuptools.setup(
    name=name,
    version=get_version(),
    description=description,
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Alibaba',
    author_email='dashscope@alibaba-inc.com',
    license='Apache 2.0',
    url=url,
    packages=setuptools.find_packages(exclude=('tests')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    platforms='Posix; MacOS X; Windows',
    python_requires='>=3.7.0',
    install_requires=get_dependencies(),
    include_package_data=True,
    zip_safe=False,
    entry_points={'console_scripts': ['dashscope = dashscope.cli:main']})
