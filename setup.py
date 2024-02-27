import setuptools
import sys
from clockwork import util

if sys.version_info < (3, 8):
    sys.exit('clockwork requires Python 3.8+ to run')

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='clockwork-kmi',
    version=util.__version__,
    author='Konrad Michalik',
    author_email='support@konradmichalik.dev',
    description='Simple DIY clock project to generate AI poems by current time.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=util.__homepage__,
    license='MIT',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: AI Poems',
        'Intended Audience :: Developers'
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'clockwork = clockwork.__main__:main'
        ]
    },
)
