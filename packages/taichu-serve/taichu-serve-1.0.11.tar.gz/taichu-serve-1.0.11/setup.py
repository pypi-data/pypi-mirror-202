from datetime import date
import sys
from setuptools import setup, find_packages
# pylint: disable = relative-import
import model_service

pkgs = find_packages()

if __name__ == '__main__':
    name = 'taichu-serve'

    requirements = ['grpcio', 'grpcio-tools', 'protobuf', 'Flask', 'gunicorn', 'Jinja2', 'Pillow']

    setup(
        name=name,
        version='1.0.11',
        description='taichu serve is a tool for serving deep learning inference',
        # long_description='',
        author='taichu platform team',
        # author_email='noreply@noreply.com',
        python_requires=">=3.6.0",
        url='',
        keywords='Serving Deep Learning Inference AI',
        packages=pkgs,
        install_requires=requirements,
        entry_points={
            'console_scripts': ['taichu-serve = model_service.command:infer_server_start']
        },
        include_package_data=True,
        # license='Apache License Version 2.0'
    )
