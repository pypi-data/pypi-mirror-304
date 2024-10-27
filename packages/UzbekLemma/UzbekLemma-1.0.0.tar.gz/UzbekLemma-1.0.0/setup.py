from setuptools import setup, find_packages

setup(
    name='UzbekLemma',
    version='1.0.0',
    author='MaksudSharipov, Dasturbek',
    author_email='sobirovogabek0409@gmail.com',
    description='Finds the lemma of Uzbek words',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ddasturbek/UzbekLemma',
    packages=find_packages(),
    install_requires=[
        'os'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
