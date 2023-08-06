from setuptools import setup

setup(
    name='gyropalm_control',
    version='1.0.0',
    description='GyroPalm Python SDK for Robotic Control using Gestures',
    packages=['gyropalm_control'],
    install_requires=[
        'websockets>=7.0',
    ],
    # other package metadata
)
