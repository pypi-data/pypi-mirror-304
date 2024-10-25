# genpybind

*Autogeneration of Python bindings from manually annotated C++ headers*

Genpybind is a tool based on [clang][] that automatically generates code to
expose a C++ API as a Python extension via [pybind11][].  Say goodbye to the
tedious task of writing and updating binding code by hand!  Genpybind ensures
that your Python bindings always stay in sync with your C++ API, complete with
docstrings, parameter names, and default arguments.  This is especially valuable
for still-evolving APIs where manual bindings can quickly become outdated.

The PyPI package is still work-in-progress, until then please take a look at
[the repo on GitHub](https://github.com/kljohann/genpybind).

[clang]: https://clang.llvm.org/
[pybind11]: https://github.com/pybind/pybind11
