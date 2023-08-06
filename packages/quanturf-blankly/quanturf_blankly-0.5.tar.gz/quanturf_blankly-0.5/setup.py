from setuptools import setup
import sys

setup_args=dict(
    name="quanturf_blankly",
    packages=['quanturf_blankly'],
    version='0.5',
    description="",
    long_description="",
    author="Quanturf",
    url="https://github.com/Quanturf/quanturf_blankly_package",
    author_email="quanturf.finance@gmail.com",
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        "console_scripts": [
            "myscript = quanturf_blankly.__main__:main",
        ]
    } 
)

if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = [
        "blankly","apscheduler","thread6","alpaca_trade_api","pandas","numpy"
    ]

def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()