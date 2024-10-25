try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name='ns-gradient',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    version='0.0.1',
    description='A package for calculating shifted gradients',
    license='MIT',
    author='Nicolus Rotich',
    author_email='nicholas.rotich@gmail.com',
    install_requires=[
    	"setuptools>=58.1.0",
    	"wheel>=0.37.1",
        "numpy>=1.26.3",
    	"pandas>=2.1.4",
        "fire"
    ],
    url='https://nkrtech.com',
    download_url='https://github.com/moinonin/ns-gradients/archive/refs/heads/main.zip',
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
)
