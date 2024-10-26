from setuptools import setup, find_packages

setup(
    name='syetodocliapp',
    version='1.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['click'],
    entry_points={
        'console_scripts':['todo=sye_todo_cli.todo:cli',]
    },
    author='Srisai Pasupuleti',
    author_email='srisaichiyan24@gmail.com',
    description='CLI Todo app with add, list, remove functionality as of now',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/srisaipasupuleti/sye_todo_cli.git",
    classifiers=[
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.0'
    
)