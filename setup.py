import setuptools

setuptools.setup(
    name="jenkins-build-export",
    version="0.0",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    license="MIT",
    python_requires=">=3.6",
    install_requires=[
        'lxml',
    ],
    entry_points=dict(
        console_scripts=[
            'jbe = jbe.__main__:main2',
        ]
    ),
    extras_require={
        'dev': [
            'httpie',
            'mypy',
        ],
    }
)
