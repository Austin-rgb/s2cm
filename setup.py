from setuptools import setup, find_packages

setup(
    name='s2cm',  # Replace with your package name
    version='0.1.0',
    description='Server to cliet messenger, for notifying clients in a client-server models',
    author='Austine Ochieng',
    author_email='prof.odhiambo.ostinel@gmail.com',
    url='https://github.com/Austin-rgb/s2cm',  # Optional
    packages=find_packages(),  # Automatically discover modules
    install_requires=[
        'requests','flask','flask-socketio'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Adjust based on your compatibility
)

