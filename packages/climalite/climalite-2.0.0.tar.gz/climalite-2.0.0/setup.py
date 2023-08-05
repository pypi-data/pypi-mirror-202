from setuptools import setup

setup(
    name='climalite',
    packages=['climalite'],
    version='2.0.0',
    license='MIT',
    description='weather forcast data',
    author_email='MichaelBitzDev@gmail.com',
    url='https://github.com/Michael-Bitz/climalite',
    keywords=['weather', 'forecast', 'openweather'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
