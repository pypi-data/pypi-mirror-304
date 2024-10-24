from setuptools import setup, find_packages
import pathlib

setup(
    name='UMP_flask',
    version='0.0.1',
    author='Mostafa Abdelsatar',
    author_email='mostafa.jamal.mjm@gmail.com',
    description='User Management Package',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    project_urls={
        'source': 'https://github.com/Mostafa1Jamal1/UMP-flask/',
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=["flask", "flask-security", "flask-mail", "mongoengine", "python-dotenv"],
    include_package_data=True,
    package_data={
        '': ['templates/security/*'],
    },
)
