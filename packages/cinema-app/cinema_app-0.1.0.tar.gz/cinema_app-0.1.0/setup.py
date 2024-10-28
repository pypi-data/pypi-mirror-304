from setuptools import setup, find_packages

setup(
    name='cinema_app',
    version='0.1.0',
    author='Dastarac Louis',
    author_email='Dastarac.louis@gmail.com',
    description='Une application pour choisir des réalisateurs de cinéma',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/votre_utilisateur/mon_projet',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
