from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='TTS_B',
    version='1.1.2',
    description='A very basic TTS tool',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',  
    author='Gowtham Venkata Raj Kumar',
    author_email='gamergowtham99@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='TTS', 
    packages=find_packages(),
    install_requires=[
        'requests',
        'playsound',
        'mutagen',
        'typing-extensions',  # Includes Union for compatibility
    ]
)
