from setuptools import setup
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open('requirements.txt', encoding="utf-8-sig") as f:
    requirements = f.readlines()


setup(
    name='fastapi_mvc_framework',
    version='1.1.6',
    license='Apache License 2.0',
    author='Bruce chou',
    author_email='smjkzsl@gmail.com',
    description='Simple and elegant use of FastApi in MVC mode',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    url='https://github.com/smjkzsl/fastapi_framework',
    packages=['fastapi_mvc_framework',],
    keywords=[
        'web framework', 'mvc framework', 'fastapi framework',
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9', 
        'Programming Language :: Python :: 3.10', 
    ],
    python_requires='>=3.6',
)
