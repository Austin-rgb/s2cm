from setuptools import find_packages, setup

setup(
    name="s2cm",
    version="0.1.0",
    description="Server to cliet messenger, for notifying clients in a client-server models",
    author="Austine Ochieng",
    author_email="prof.odhiambo.ostinel@gmail.com",
    maintainer="Austin-rgb",
    maintainer_email="prof.odhiambo.ostine@gmail.com",
    url="https://github.com/Austin-rgb/s2cm",
    packages=find_packages(),
    download_url="https://github.com/Austin-rgb/s2cm/releases",
    install_requires=[
        "bcrypt",
        "peewee",
        "requests",
        "flask",
        "flask-socketio",
        "socketio",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
