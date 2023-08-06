from __future__ import division, absolute_import, print_function
from setuptools import find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop
from numpy.distutils.core import Extension, setup
import unittest
import pathlib

locscale_path = pathlib.Path(__file__).parent.resolve()

ex1 = Extension(name='fcodes_fast',
                sources=['locscale/include/symmetry_emda/fcodes_fast.f90'])

long_description = (locscale_path / "README.md").read_text()


def get_version():
    version_text = (locscale_path / "locscale" / "__version__.py").read_text()
    version = version_text.split("=")[1][1:-1]
    return version


def locscale_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


class PostDevelopCommand(develop):
    """ Post-installation for development mode. """

    def run(self):
        develop.run(self)

        from subprocess import run
        from shutil import which

        # Install conda packages
        run(["conda", "install", "-c", "conda-forge", "cudatoolkit=11.3.1", "--yes"])
        run(["conda", "install", "-c", "conda-forge", "cudnn=8.2.1", "--yes"])
        run(["conda", "install", "-c", "conda-forge", "openmpi=4.1.2", "--yes"])
        run(["conda", "install", "-c", "conda-forge", "mpi4py=3.1", "--yes"])

        # Check if refmac5 is installed
        refmac5_path = which("refmac5")
        if refmac5_path is None:
            raise UserWarning(
                "Refmac5 is not installed. Please install it and try again.")
        else:
            print("Refmac5 is installed at {}".format(refmac5_path))
            print("If you want to use a different binary please use the --refmac5_path option or alias it to refmac5")


class PostInstallCommand(install):
    """Post-installation for installation mode."""

    def run(self):
        install.run(self)

        from subprocess import run
        from shutil import which

        # Install conda packages
        run(["conda", "install", "-c", "conda-forge", "cudatoolkit=11.3.1", "--yes"], check=True)
        run(["conda", "install", "-c", "conda-forge", "cudnn=8.2.1", "--yes"], check=True)
        run(["conda", "install", "-c", "conda-forge", "openmpi=4.1.2", "--yes"], check=True)
        run(["conda", "install", "-c", "conda-forge", "mpi4py=3.1", "--yes"], check=True)

        # Check if refmac5 is installed
        refmac5_path = which("refmac5")
        if refmac5_path is None:
            raise UserWarning(
                "Refmac5 is not installed. Please install CCP4 before running locscale. Without Refmac locscale cannot refine the input atomic structure.")
        else:
            print("Refmac5 is installed at {}".format(refmac5_path))
            print("If you want to use a different binary please use the --refmac5_path option or alias it to refmac5")


setup(name='locscale',
      version=get_version(),
      author='Alok Bharadwaj, Arjen J. Jakobi, Reinier de Bruin',
      url='https://gitlab.tudelft.nl/aj-lab/locscale',
      project_urls={
          "Bug Tracker": "https://gitlab.tudelft.nl/aj-lab/locscale/issues",
      },
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Science/Research",
          "Topic :: Scientific/Engineering",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "License :: OSI Approved :: BSD License",
      ],
      description='Contrast optimization for cryo-EM maps',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='3-clause BSD',
      packages=find_packages(),
      include_package_data=True,
      package_data={'locscale': ['utils/*.pickle', 'include/symmetry_emda/*.f90',
                                 'emmernet/emmernet_models/*.tar.gz', 'emmernet/emmernet_models/*.hdf5']},
      install_requires=['matplotlib>=3.3.4', 'biopython>=1.78', 'numpy==1.19.2', 'scipy>=1.5.4', 'pandas>=1.1.5',
                        'mrcfile>=1.3.0', 'gemmi>=0.4.8', 'pypdb==2.0', 'scikit-learn', 'pwlf>=2.0.4', 'tqdm>=4.62.3',
                        'more_itertools>=8.10.0', 'servalcat>=0.2.23', 'tensorflow==2.6', 'tensorflow-addons==0.14.0',
                        'keras==2.6.0', 'tensorflow_datasets==4.5.2', 'pyfiglet>=0.8.post1', 'wget>=3.2', 'seaborn>=0.11', 'locscale'],
      extras_require={'mac': ['tensorflow-macos==2.7', 'tensorflow-metal']},
      entry_points={
          'console_scripts': [
              'locscale = locscale.main:main',
          ],
      },
      test_suite='setup.locscale_test_suite',
      ext_modules=[ex1],
      cmdclass={'develop': PostDevelopCommand,
                'install': PostInstallCommand},

      zip_safe=False)
