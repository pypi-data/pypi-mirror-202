from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='PyDesmos',
    version='0.0.2',
    description='An easy-to-use python to desmos html compiler via the desmos api.',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Lyam Boylan',
    author_email='lyamboylan@gmail.com',
    license='MIT',
    keywords=['math', 'graph', 'desmos', 'graphing software', 'html', 'sympy'],
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=['sympy']
)