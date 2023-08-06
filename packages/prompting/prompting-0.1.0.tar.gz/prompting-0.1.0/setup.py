from setuptools import setup

setup(name='prompting',
      version='0.1.0',
      description='This module provides iPython integration and magics that allow prompting.',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      readme = "README.md",
      url='https://gitlab.com/mcaledonensis/magickey/-/tree/prompting',
      author='Merlinus Caledonensis',
      author_email='merlin@roundtable.game',
      license='Apache 2.0',
      packages=['prompting', 'prompting/prompts'],
      package_data={'': ['prompts/meta_prompt.txt', 'prompts/system_prompt.txt']},
      include_package_data=True,
      install_requires=['openai', 'parsimonious'],
      zip_safe=False)
