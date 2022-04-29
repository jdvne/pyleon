from setuptools import setup
import os

# long_description = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

os.system('cd leon && sh INSTALL')

setup(
    # Package description
    name = "pyleon",
    version = "0.0.1",
    description = 'An experimental python wrapper for leon',
    # long_description = long_description,
    license = 'AGPLv3',
    author = 'Joshua Devine, Ian Switzer, leon team, gatb-tools team',
    author_email = 'josh@devines.org',
    classifiers=[
        # Topic
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Audience
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Education',

        'License :: OSI Approved :: GNU Affero General Public License v3',

        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Environnement, OS, languages
        'Environment :: Console',

        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: POSIX',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: C++',
    ],
)