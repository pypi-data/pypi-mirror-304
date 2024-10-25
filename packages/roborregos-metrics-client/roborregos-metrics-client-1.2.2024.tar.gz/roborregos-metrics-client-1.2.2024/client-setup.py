from setuptools import setup, find_packages

setup(
    name='roborregos-metrics-client',
    version='1.2.2024',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pydantic',
        'psutil',
    ],
    entry_points={
        'console_scripts': [
            'robometrics-worker = robometrics.worker.worker:main',
            'robometrics-sync   = robometrics.worker.worker:sync'
        ]
    }
)
