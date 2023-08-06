from setuptools import setup, find_packages

setup(
    name='django-mapper',
    version='0.1.0',
    description='A utility class for mapping data between Django models',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/django-mapper',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
        'Django>=2.2',
    ],
)

