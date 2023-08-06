from setuptools import setup, find_packages


setup(name='admin_tool_button',
     version='1.0.1-alpha',
     description='Extra tool buttons for Django admin',
     long_description=open('README.md').read().strip(),
     long_description_content_type="text/markdown",
     author='Bram Boogaard',
     author_email='padawan@hetnet.nl',
     url='https://github.com/bboogaard/admin_tool_button',
     packages=find_packages(include=['admin_tool_button']),
     install_requires=[
         'pytest',
         'pytest-cov',
         'pytest-django==4.5.2',
         'django==3.2'
     ],
     license='MIT License',
     zip_safe=False,
     keywords='Django Admin',
     classifiers=['Development Status :: 3 - Alpha'])
