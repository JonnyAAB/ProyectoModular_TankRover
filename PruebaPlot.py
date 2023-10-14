import matplotlib.pyplot as plt

plt.plot([1,2,3,4])
plt.show()

Preparing metadata (pyproject.toml) ... error
  error: subprocess-exited-with-error
  
  × Preparing metadata (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [53 lines of output]
      + /usr/bin/python3 /tmp/pip-install-te7iektm/numpy_96aa0e77d51b48ecad951557899c2d17/vendored-meson/meson/meson.py setup /tmp/pip-install-te7iektm/numpy_96aa0e77d51b48ecad951557899c2d17 /tmp/pip-install-te7iektm/numpy_96aa0e77d51b48ecad951557899c2d17/.mesonpy-2qdu864b/build -Dbuildtype=release -Db_ndebug=if-release -Db_vscrt=md --native-file=/tmp/pip-install-te7iektm/numpy_96aa0e77d51b48ecad951557899c2d17/.mesonpy-2qdu864b/build/meson-python-native-file.ini
      The Meson build system
      Version: 1.2.99
      Source dir: /tmp/pip-install-te7iektm/numpy_96aa0e77d51b48ecad951557899c2d17
      Build dir: /tmp/pip-install-te7iektm/numpy_96aa0e77d51b48ecad951557899c2d17/.mesonpy-2qdu864b/build
      Build type: native build
      Project name: NumPy
      Project version: 1.26.1
      C compiler for the host machine: cc (gcc 10.2.1 "cc (Raspbian 10.2.1-6+rpi1) 10.2.1 20210110")
      C linker for the host machine: cc ld.bfd 2.35.2
      C++ compiler for the host machine: c++ (gcc 10.2.1 "c++ (Raspbian 10.2.1-6+rpi1) 10.2.1 20210110")
      C++ linker for the host machine: c++ ld.bfd 2.35.2
      Cython compiler for the host machine: cython (cython 3.0.3)
      Host machine cpu family: arm
      Host machine cpu: armv7l
      Program python found: YES (/usr/bin/python3)
      Found pkg-config: /usr/bin/pkg-config (0.29.2)
      Run-time dependency python found: YES 3.9
      Has header "Python.h" with dependency python-3.9: YES
      Compiler for C supports arguments -fno-strict-aliasing: YES
      Message: During parsing cpu-dispatch: The following CPU features were ignored due to platform incompatibility or lack of support:
      "XOP FMA4"
      Test features "NEON" : Supported
      Test features "NEON_FP16" : Supported
      Test features "NEON_VFPV4" : Supported
      Test features "ASIMD" : Unsupported due to Compiler fails against the test code of "ASIMD"
      Test features "ASIMDHP" : Unsupported due to Implied feature "ASIMD" is not supported
      Test features "ASIMDFHM" : Unsupported due to Implied feature "ASIMD" is not supported
      Configuring npy_cpu_dispatch_config.h using configuration
      Message:
      CPU Optimization Options
        baseline:
          Requested : min
          Enabled   :
        dispatch:
          Requested : max -xop -fma4
          Enabled   : NEON NEON_FP16 NEON_VFPV4
      
      Library m found: YES
      Did not find CMake 'cmake'
      Found CMake: NO
      Run-time dependency scipy-openblas found: NO (tried pkgconfig and cmake)
      Run-time dependency mkl found: NO (tried pkgconfig and system)
      Run-time dependency mkl found: NO (tried pkgconfig and system)
      Run-time dependency accelerate found: NO (tried system)
      Run-time dependency openblas found: NO (tried pkgconfig, pkgconfig, pkgconfig, system and cmake)
      Run-time dependency flexiblas found: NO (tried pkgconfig and cmake)
      Run-time dependency blis found: NO (tried pkgconfig and cmake)
      Run-time dependency blas found: NO (tried pkgconfig and cmake)
      
      ../../numpy/meson.build:169:4: ERROR: Problem encountered: No BLAS library detected! Install one, or use the `allow-noblas` build option (note, this may be up to 100x slower for some linear algebra operations).
      
      A full log can be found at /tmp/pip-install-te7iektm/numpy_96aa0e77d51b48ecad951557899c2d17/.mesonpy-2qdu864b/build/meson-logs/meson-log.txt
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.
