from setuptools import setup, find_packages

# Read in the README for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sgmse',  # Package name
    version='0.1.0',  # Initial version
    author='Signal Processing (SP), Universität Hamburg',  # Author details
    author_email='sp-office.inf@uni-hamburg.de',  # Author email
    description='Speech enhancement model using SGMSE',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sp-uhh/sgmse',  # GitHub repo URL
    project_urls={
        "Source Code": "https://github.com/sp-uhh/sgmse",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license="MIT",  # License type
    packages=find_packages(),  # Automatically find packages
    python_requires='>=3.6',  # Minimum Python version
    install_requires=[
        'gdown',
        'h5py',
        'ipympl',
        'librosa',
        'ninja',
        'numpy<2.0',
        'pandas',
        'pesq',
        'pillow',
        'protobuf',
        'pyarrow',
        'pyroomacoustics',
        'pystoi',
        'pytorch-lightning',
        'scipy',
        'sdeint',
        'setuptools',
        'seaborn',
        'torch',
        'torch-ema',
        'torch-pesq',
        'torchaudio',
        'torchvision',
        'torchinfo',
        'torchsde',
        'tqdm',
        'wandb',
    ],
    include_package_data=True,  # Include non-code files like README
)
