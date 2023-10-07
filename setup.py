with open('requirements.txt') as f:
    content = f.readlines()
requirements = [x.strip() for x in content]

setuptools.setup(name='lrisks',
version='0.1',
description='Probability functions for the l-risk calculator',
url='#',
author='Arepo',
install_requires=requirements,
author_email='',
packages=setuptools.find_packages(),
zip_safe=False)
