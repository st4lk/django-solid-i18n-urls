from setuptools import setup, find_packages
from solid_i18n import __author__, __version__

setup(
    name='django-solid-i18n-urls',
    version=__version__,
    packages=find_packages(),
    keywords='django, i18n, urls, solid, redirects',
    include_package_data=True,
    license='BSD License',
    package_dir={'solid_i18n': 'solid_i18n'},
    description='Django i18n middleware and url pattern without redirects',
    long_description=open('README.md').read(),
    url='http://www.lexev.org/',
    author=__author__,
    author_email='alexevseev@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
