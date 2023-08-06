'''
setup for the tools
'''
import os
from setuptools import setup, find_packages



if os.environ.get('CONVERT_README'):
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
else:
    long_description = ''

install_requires = ['openai', 'subprocess_tee', 'glom==23.3.0', 'bashlex==0.18', 'psutil', 'colorama', 'pyte==0.8.1']
extras_require = {':python_version<"3.4"': ['pathlib2']}

setup(name='unifix',
      version= '0.1.1',
      description="Magnificent app which corrects your previous console command",
      long_description=long_description,
      author='Mengyu Yao',
      author_email='191840305@smail.nju.com',
      url='',
      license='MIT',
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require=extras_require,
      python_requires='>=3.3',
      packages=find_packages(exclude=['evaluation', 
                                      'tests', 'tests.*', 'baseline-dist']),
      entry_points={'console_scripts': ['unifix = UniFix.UniFix:main']}
      )