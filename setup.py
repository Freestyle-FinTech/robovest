from setuptools import setup

setup(
    name='robovest',
    packages=['robovest'],
    include_package_data=True,
    install_requires=[
        'flask','nltk',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
