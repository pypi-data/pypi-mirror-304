from setuptools import setup, find_packages
setup(
    name='ec_metrics',
    version='0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ec_metrics=ec_metrics.__main__:main'
        ],
    },
    author="Анастасия Колесникова",
    description="Пакет для расчета чистой прибыли и рентабельности инвестиций (ROI).",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/finance_metrics",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
