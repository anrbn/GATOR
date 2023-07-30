from setuptools import setup, find_packages

requirements = [
    "cachetools==5.3.1",
    "certifi==2023.5.7",
    "cffi==1.15.1",
    "charset-normalizer==3.2.0",
    "cryptography==41.0.2",
    "gator==0.1",
    "google-api-core==2.11.1",
    "google-api-python-client==2.94.0",
    "google-auth==2.22.0",
    "google-auth-httplib2==0.1.0",
    "google-auth-oauthlib==1.0.0",
    "google-cloud-core==2.3.3",
    "google-cloud-storage==2.10.0",
    "google-crc32c==1.5.0",
    "google-resumable-media==2.5.0",
    "googleapis-common-protos==1.59.1",
    "httplib2==0.22.0",
    "idna==3.4",
    "jsonpickle==3.0.1",
    "oauthlib==3.2.2",
    "protobuf==4.23.4",
    "pyasn1==0.5.0",
    "pyasn1-modules==0.3.0",
    "pycparser==2.21",
    "pyOpenSSL==23.2.0",
    "pyparsing==3.1.0",
    "requests==2.31.0",
    "requests-oauthlib==1.3.1",
    "rsa==4.9",
    "six==1.16.0",
    "termcolor==2.3.0",
    "uritemplate==4.1.1",
    "urllib3==1.26.16"
]

setup(
    name='gator',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'gator=gator.main:main',
        ],
    },
)
