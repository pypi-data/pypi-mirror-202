from setuptools import setup, find_packages

VERSION = '0.01'
DESCRIPTION = 'A Python for playing audio from text and saving it to a file'
LONG_DESCRIPTION = 'A Python module for playing audio from text and saving it to a file using Google Text-to-Speech API'

setup(
    name='playfromtext',
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='http://github.com/tushark39',
    author='Priyanshu Patel',
    author_email='priyanshupatel.hawk@gmail.com',
    license='MIT',
    install_requires=['playsound==1.2.2', 'gtts==2.2.2'],
    packages=find_packages(),
    keywords=['python', 'playfromtext', 'play', 'audio', 'text', 'tts', 'google', 'text-to-speech', 'speech', 'audio', 'play', 'playfromtext'],
    entry_points={
        'console_scripts' : [
            'playfromtext = playfromtext.__init__:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Multimedia :: Sound/Audio :: Players',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
        'Topic :: Utilities',
    ],

)
