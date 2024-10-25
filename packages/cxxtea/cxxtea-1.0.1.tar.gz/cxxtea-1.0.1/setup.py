from setuptools import setup, Extension
from wheel.bdist_wheel import bdist_wheel

class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp"):
            return "cp36", "abi3", plat

        return python, abi, plat

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="cxxtea",
    version="1.0.1",
    author='wood',
    author_email='miraclerinwood@gmail.com',
    url='https://github.com/ifduyue/cxxtea',
    description="cxxtea is a simple block cipher implemented in C",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="BSD",
    ext_modules=[
        Extension(
            "cxxtea",
            sources=["cxxtea.c"],
            define_macros=[("Py_LIMITED_API", "0x03060000")],
            py_limited_api=True,
        )
    ],
    cmdclass={"bdist_wheel": bdist_wheel_abi3},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
    ],
    python_requires=">=3.6",
)
