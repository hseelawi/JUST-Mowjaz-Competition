from setuptools import setup, find_packages

setup(
    name='Mowjaz Topics',
    version='JUST_competition',
    description="Perform topic classification for Mowjaz project",
    author='Mowjaz ML Team',
    license='Proprietary: public use',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Natural Language :: Arabic',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='Mawdoo3 NLP',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'flask',
        'joblib',
        'numpy',
        'sklearn',
        'tensorflow',
        'gensim',
        'pyarabic',
        'jupyter',
        'pandas',
    ],
    extras_require={
        'dev': ['nose2', 'requests', 'pylint'],
    },
    test_suite='nose2.collector.collector',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'start_microservice=api:launch_the_app',
        ],
    },
)
