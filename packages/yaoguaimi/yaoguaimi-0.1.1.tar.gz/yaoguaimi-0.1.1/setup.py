import setuptools

with open("README.md","r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='yaoguaimi',  # 替换为你项目的名称
    version='0.1.1',
    include_package_data=True,
    author='hzx',
    author_email='hzx802502@gmail.com',
    description='A package with Jupyter Notebook code for machine learning tasks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),  # 自动发现项目中的包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
    ],
)
