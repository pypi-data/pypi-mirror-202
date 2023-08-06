from setuptools import setup, find_packages


setup(
    name='external_requests',
    version='1.0.0',
    author='Venfi Oranai',
    author_email='venfioranai@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://gitlab.com/VenfiOranai/external-requests',
    install_requires=[
        'marshmallow',
        'requests'
    ]
)
