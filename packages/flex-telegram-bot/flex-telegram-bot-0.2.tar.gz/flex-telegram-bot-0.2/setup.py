from setuptools import setup, find_packages

setup(
    name='flex-telegram-bot',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='Esnek Türkçe Telegram bot kütüphanesi.',
    author='FlexN01',
    author_email='v.flexn01@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
