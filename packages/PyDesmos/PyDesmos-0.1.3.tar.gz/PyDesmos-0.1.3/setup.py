from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='PyDesmos',
    version='0.1.3',
    description='An easy-to-use Python to Desmos graph HTML compiler via the Desmos API (with OEIS support).',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Lyam Boylan',
    author_email='lyamboylan@gmail.com',
    license='MIT',
    keywords=['math', 'graph', 'desmos', 'graphing software', 'html', 'sympy', 'api', 'oeis'],
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=['sympy', 'requests']
)