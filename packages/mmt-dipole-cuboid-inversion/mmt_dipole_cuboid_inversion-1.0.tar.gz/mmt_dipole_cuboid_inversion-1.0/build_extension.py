import setuptools
from setuptools.extension import Extension
from setuptools.dist import Distribution
# from Cython.Distutils import build_ext
# setuptools contains the correct self.build_extensions function when
# writing our own custom_build_ext function:
# This might help: https://github.com/cython/cython/blob/master/docs/src/tutorial/appendix.rst
from setuptools.command.build_ext import build_ext
# cython and python dependency is handled by pyproject.toml
from Cython.Build import cythonize
import numpy
import os
from os.path import join as pjoin


# -----------------------------------------------------------------------------
# CUDA SPECIFIC FUNCTIONS

def find_in_path(name, path):
    "Find a file in a search path"
    # adapted fom http://code.activestate.com/recipes/52224-find-a-file-given-a-search-path/
    for dir in path.split(os.pathsep):
        binpath = pjoin(dir, name)
        if os.path.exists(binpath):
            return os.path.abspath(binpath)
    return None


def locate_cuda():
    """Locate the CUDA environment on the system

    Returns a dict with keys 'home', 'nvcc', 'include', and 'lib64'
    and values giving the absolute path to each directory.

    Starts by looking for the CUDAHOME env variable. If not found, everything
    is based on finding 'nvcc' in the PATH.
    """

    # first check if the CUDAHOME env variable is in use
    if 'CUDAHOME' in os.environ:
        home = os.environ['CUDAHOME']
        nvcc = pjoin(home, 'bin', 'nvcc')
    else:
        # otherwise, search the PATH for NVCC
        nvcc = find_in_path('nvcc', os.environ['PATH'])
        if nvcc is None:
            # raise EnvironmentError('The nvcc binary could not be '
            #     'located in your $PATH. Either add it to your path, or set $CUDAHOME')
            return False

        home = os.path.dirname(os.path.dirname(nvcc))

    cudaconfig = {'home': home, 'nvcc': nvcc, 'include': pjoin(home, 'include'),
                  'lib64': pjoin(home, 'lib64')}

    for k, v in cudaconfig.items():
        if not os.path.exists(v):
            # raise EnvironmentError('The CUDA %s path could not be located in %s' % (k, v))
            return False

    return cudaconfig


CUDA = locate_cuda()
# print(CUDA)


def customize_compiler_for_nvcc(self):
    """inject deep into distutils to customize how the dispatch
    to gcc/nvcc works.

    If you subclass UnixCCompiler, it's not trivial to get your subclass
    injected in, and still have the right customizations (i.e.
    distutils.sysconfig.customize_compiler) run on it. So instead of going
    the OO route, I have this. Note, it's kindof like a wierd functional
    subclassing going on."""

    # tell the compiler it can processes .cu
    self.src_extensions.append('.cu')

    # save references to the default compiler_so and _comple methods
    default_compiler_so = self.compiler_so
    super = self._compile

    # now redefine the _compile method. This gets executed for each
    # object but distutils doesn't have the ability to change compilers
    # based on source extension: we add it.
    def _compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
        if os.path.splitext(src)[1] == '.cu':
            # use the cuda for .cu files
            self.set_executable('compiler_so', CUDA['nvcc'])
            # use only a subset of the extra_postargs, which are 1-1 translated
            # from the extra_compile_args in the Extension class
            postargs = extra_postargs['nvcc']
        else:
            postargs = extra_postargs['gcc']

        super(obj, src, ext, cc_args, postargs, pp_opts)
        # reset the default compiler_so, which we might have changed for cuda
        self.compiler_so = default_compiler_so

    # inject our redefined _compile method into the class
    self._compile = _compile


# run the customize_compiler
class custom_build_ext(build_ext):
    def build_extensions(self):
        customize_compiler_for_nvcc(self.compiler)
        build_ext.build_extensions(self)


# -----------------------------------------------------------------------------
# Compilation of CPP modules

# Define .cpp .c aguments passed to the compiler
# If using cuda, we set a dictionary to use different arguments for nvcc
# (see custom compiler)
if CUDA:
    com_args = dict(gcc=['-O3', '-fopenmp'])
else:
    com_args = ['-std=c99', '-O3', '-fopenmp']

link_args = ['-fopenmp']

extensions = [
    Extension("mmt_dipole_cuboid_inversion.cython_lib.pop_matrix_lib",
              ["mmt_dipole_cuboid_inversion/cython_lib/pop_matrix_lib.pyx",
               "mmt_dipole_cuboid_inversion/cython_lib/pop_matrix_C_lib.c"],
              extra_compile_args=com_args,
              extra_link_args=link_args,
              include_dirs=[numpy.get_include()])
]

if CUDA:
    # Add cuda options to the com_args dict and the extra library
    #
    # This syntax is specific to this build system
    # We're only going to use certain compiler args with nvcc and not with gcc
    # the implementation of this trick is in customize_compiler() below
    # For nvcc we use the Turing architecture: sm_75
    # See: https://arnon.dk/matching-sm-architectures-arch-and-gencode-for-various-nvidia-cards/
    # FMAD (floating-point multiply-add): turning off helps for numerical precission (useful
    #                                     for graphics) but this might slightly affect performance
    com_args['nvcc'] = ['-arch=sm_75', '--fmad=false', '--ptxas-options=-v',
                        '-c', '--compiler-options', "'-fPIC'"]

    extensions.append(
        Extension("dipole_cuboid_inversion.cython_cuda_lib.pop_matrix_cudalib",
                  sources=["dipole_cuboid_inversion/cython_cuda_lib/pop_matrix_cudalib.pyx",
                           "dipole_cuboid_inversion/cython_cuda_lib/pop_matrix_cuda_lib.cu"],
                  # library_dirs=[CUDA['lib64']],
                  libraries=['cudart'],
                  language='c++',
                  extra_compile_args=com_args,
                  include_dirs=[numpy.get_include(), CUDA['include'], '.'],
                  library_dirs=[CUDA['lib64']],
                  runtime_library_dirs=[CUDA['lib64']])
    )

# -----------------------------------------------------------------------------

if CUDA is False:
    print("CUDAHOME env variable or CUDA not found: skipping cuda extensions")
    cmdclass = {'build_ext': build_ext}
else:
    cmdclass = {'build_ext': custom_build_ext}

# -----------------------------------------------------------------------------

# For now we do not need a custom BuildExt class
# class BuildExt(build_ext):
#     def build_extensions(self):
#         try:
#             if CUDA is not False:
#                 print('Here')
#                 customize_compiler_for_nvcc(super().compiler)
#                 super().build_extension(self)
#                 super().run()
#             else:
#                 super().build_extensions(self)
#         except Exception:
#             pass

# We are assuming Cython IS installed, otherwise, see solution at
# https://github.com/davidcortesortuno/oommfpy/blob/master/build.py
# def build(setup_kwargs):
#     setup_kwargs.update(
#         dict(
#             cmdclass=dict(build_ext=cmdclass['build_ext']),
#             ext_modules=cythonize(extensions,
#                                   language_level=3,
#                                   ),
#             zip_safe=False
#         )
#     )

# Source: https://stackoverflow.com/questions/60501869/poetry-cython-tests-nosetests
# distutils magic. This is essentially the same as calling
# python setup.py build_ext --inplace
dist = Distribution(attrs=dict(cmdclass=dict(build_ext=cmdclass['build_ext']),
                               ext_modules=cythonize(extensions,
                                                     language_level=3),
                               zip_safe=False)
                    )
build_ext_cmd = dist.get_command_obj('build_ext')
build_ext_cmd.ensure_finalized()
build_ext_cmd.inplace = 1
build_ext_cmd.run()
