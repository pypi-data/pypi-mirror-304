from setuptools import setup

setup(
    name='ani-shedule',
    version='1.4',
    description='A simple to view anime aring date and upcoming anime.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Kamanati/Ani-Shedule',
    author='Hasan',
    author_email='yfor22971@gmail.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'tqdm==4.63.0',
        'lxml==5.2.2',
        'requests==2.32.3',
        'prompt-toolkit==3.0.43',
    ],
    entry_points={
        'console_scripts': [
            'ani-shedule=shedule:main', 
        ],
    },
)
