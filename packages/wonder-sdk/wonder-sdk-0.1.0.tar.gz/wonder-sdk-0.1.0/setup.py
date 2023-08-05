from setuptools import setup

setup(
    name='wonder-sdk',
    version='0.1.0',
    description='Python SDK for Firebase and Google Cloud Platform services',
    author='basri',
    author_email='basri@wonder.co',
    packages=['wonder_sdk'],
    install_requires=[
      'firebase-admin==6.0.1'
      'google-cloud-pubsub==2.13.11',
      'google-cloud-storage==2.7.0',
      'google-cloud-translate==3.8.4',
    ],
)