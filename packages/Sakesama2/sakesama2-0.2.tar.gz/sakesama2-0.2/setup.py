from setuptools import setup, find_packages

setup(
    name="Sakesama2",
    version="0.2",
    author="KaijaKuri",
    author_email="example@gmail.com",
    description="This is a speech to text package created by your Kaijakuri",
    
)
packages = find_packages(),
install_requires=[
        'selenium',
        'webdriver_manager',
    ]