"""

import os
base_path = os.path.abspath(os.path.dirname(__file__))


def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs
    config = Configuration('two_dim', parent_package, top_path)
    config = Configuration('three_dim', parent_package, top_path)


    return config
if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(maintainer='riyazi Developers',
          maintainer_email='riyazi@gmail.com',
          description='Geometry',
          url='#',
          license='BSD 3 Clause',
          **(configuration(top_path='').todict())
          )
"""