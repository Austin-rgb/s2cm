from setuptools import find_packages, setup

long_description = None
with open("README.md", "r+", encoding="utf-8") as ld:
    long_description = ld.read()
setup(
    name="s2cm",
    version="0.4.1",
    description="Server to cliet messenger, for notifying clients in a client-server models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
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
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
