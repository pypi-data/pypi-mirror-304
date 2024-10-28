from setuptools import setup, find_packages
from mlagents.plugins import ML_AGENTS_STATS_WRITER

setup(
    name="mlagents_sps_plugin",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "mlagents>=0.30.0",
        "torch",
        "tensorboard",
    ],
    entry_points={
        ML_AGENTS_STATS_WRITER: [
            "sps_writer=mlagents_sps_plugin.sps_stats_writer:get_sps_stats_writer"
        ]
    },
    author="Louis Gauthier",
    author_email="louis@dgwave.net",
    description="A plugin for Unity ML-Agents to log Steps Per Second (SPS) to TensorBoard",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/louisgthier/mlagents-sps-plugin",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.6",
)
