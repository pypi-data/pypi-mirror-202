from setuptools import setup

__version__ = "1.0.0"

setup(
    name='arrendatools_ipc',
    version=__version__,
    description='Módulo de Python que realiza la actualización de rentas de alquiler por anualidades completas con el IPC (LAU) descrita en la web del INE de España. ',
    url='https://github.com/hokus15/ArrendaToolsIPC',
    author='hokus15',
    author_email='hokus@hotmail.com',
    license='MIT',
    packages=['arrendatools_ipc'],
    install_requires=['requests>=2.28.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
