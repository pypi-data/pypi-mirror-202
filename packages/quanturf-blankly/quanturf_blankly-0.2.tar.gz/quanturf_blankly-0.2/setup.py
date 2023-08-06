from setuptools import setup
import sys

setup_args=dict(
    name="quanturf_blankly",
    packages=['quanturf_blankly'],
    version='0.2',
    description="",
    long_description="",
    author="Quanturf",
    url="https://github.com/Quanturf/quanturf_blankly_package",
    author_email="quanturf.finance@gmail.com",
      entry_points={
        "console_scripts": [
            "myscript = quanturf_blankly.__main__:main",
        ]
    } 
)

if 'setuptools' in sys.modules:
    setup_args['install_requires'] = install_requires = [
        "blankly","apscheduler","alpaca_trade_api","pandas","numpy"
    ]

def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()