from setuptools import setup, find_packages

setup(
    name='viturka-nn',
    version='0.1.0',
    description='A client library for deep federated learning platform.',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    install_requires=[
        'numpy==1.24.3',  # Example of dependencies
        'pandas',
        'torch',
        'torchvision',
        'pycocotools',
        'scikit-learn'
    ],
    python_requires='>=3.6'
)