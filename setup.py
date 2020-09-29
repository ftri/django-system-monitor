from setuptools import setup, find_packages
import os

setup(
    name='django-system-monitor',
    version='0.6',
    author='Frédéric TRIBEL',
    author_email='frederic.tribel@gmail.com',
    url='https://github.com/ftri/django-system-monitor',
    description='View simple system statistics in django admin panel',
    long_description=os.path.join(os.path.dirname(__file__), 'README.md'),
    packages=find_packages(exclude=[]),
    install_requires=[
        'psutil==5.7.2',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
