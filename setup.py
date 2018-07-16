from setuptools import find_packages, setup

setup(
    name="ereuse-rate",
    version='0.0.2',
    packages=find_packages(),
    url='https://github.com/ereuse/rate',
    license='Affero',
    author='eReuse.org team',
    author_email='x.bustamante@ereuse.org',
    description='',
    install_requires=[
        'pytest'
    ],
    tests_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
