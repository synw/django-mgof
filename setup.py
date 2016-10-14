from setuptools import setup, find_packages


version = __import__('mgof').__version__

setup(
  name = 'django-mgof',
  packages=find_packages(),
  include_package_data=True,
  version = version,
  description = 'Modern good old forums for Django',
  author = 'synw',
  author_email = 'synwe@yahoo.com',
  url = 'https://github.com/synw/django-mgof', 
  download_url = 'https://github.com/synw/django-mgof/releases/tag/'+version, 
  keywords = ['django', 'forum'], 
  classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
  zip_safe=False,
  install_requires=[
        'bleach',
        'django-braces',
        'django-ckeditor',
        'django-mbase',
        'django-mqueue',
    ],
)
