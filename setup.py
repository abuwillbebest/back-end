from distutils.core import setup
import glob

setup(name='novel',
      version='1.0',
      description='novel web + python crawl',
      author='Wayne',
      author_email='sagezeng@foxmail.com',
      url='',
      packages=['novel_web', 'post', 'user'],
      py_modules=['manage'],
      data_files=glob.glob('templates/*.html') + ['requirements']
      )
