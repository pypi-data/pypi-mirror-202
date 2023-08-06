from setuptools import setup, find_packages

setup(
    name='devops_my_pckg_test_123',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
	'numpy'
    ],
    description='My first Python package',
    author='Ulises',
    author_email='ulises.st.99@gmail.com',
    #url='https://github.com/your_username/your_package',
)
