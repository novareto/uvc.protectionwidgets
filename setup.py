# -*- coding: utf-8 -*-
# Copyright (c) 2008-2013 Infrae. All rights reserved.
# See also LICENSE.txt

from setuptools import setup, find_packages
import os

version = '1.0.3.dev0'

tests_require = [
    ]

zeam_requires = [
    'zeam.form.base',
    'zeam.form.ztk',
]

dolmen_requires = [
    'dolmen.forms.base',
    'dolmen.forms.ztk',
]

setup(name='uvc.protectionwidgets',
      version=version,
      description="Captcha Widget for UVCSite",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        ],
      keywords='captcha',
      author='Christian Klinger',
      author_email='ck@novareto.de',
      url='',
      license='BSD',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      namespace_packages=['uvc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'norecaptcha',
        'zope.i18n',
        'zope.component',
        'zope.interface',
        'zope.schema',
        'zope.traversing',
        ],
      entry_points="""
      # -*- Entry points: -*-
      [zeam.form.components]
      captcha = uvc.protectionwidgets.widgets.captcha:register
      [dolmen.collection.components]
      captcha = uvc.protectionwidgets.widgets.captcha:register
      """,
      tests_require = tests_require,
      extras_require = {
          'test': tests_require,
          'zeam': zeam_requires,
          'dolmen': dolmen_requires,
      })
