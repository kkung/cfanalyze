from setuptools import setup, find_packages

setup(
    name='CFAnalyze',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['boto>=2.5.2'],
    entry_points={
        'console_scripts': ['cfa = cfanalyze.__main__:main']
    },
    author='MinYoung Jung',
    author_email='kkungkkung@gmail.com',
    description='Just Simple Amazon CloudFront Access Log Analyzer',
    long_description=open('README').read(),
    url='https://github.com/kkung/cfanalyze',
    keywords='aws cloudfront cf analyze',
    license='MIT License',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'])
