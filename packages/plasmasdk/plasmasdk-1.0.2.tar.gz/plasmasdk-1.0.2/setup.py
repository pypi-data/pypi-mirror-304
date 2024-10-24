from setuptools import setup, find_packages
import re
import ast

def get_version_string():
    """
    Get the gne version number
    :return: version number
    :rtype: str
    """
    with open("plasmasdk/__init__.py", "rb") as _f:
        version_line = re.search(
            r"__version__\s+=\s+(.*)", _f.read().decode("utf-8")
        ).group(1)
        return str(ast.literal_eval(version_line))


def get_author_string():
    """
    Get the gne author info
    :return: author name
    :rtype: str
    """
    with open("plasmasdk/__init__.py", "rb") as _f:
        version_line = re.search(
            r"__author__\s+=\s+(.*)", _f.read().decode("utf-8")
        ).group(1)
        return str(ast.literal_eval(version_line))


with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='plasmasdk',
    packages=find_packages(exclude=[]),
    install_requires=['pandas', 'numpy'],
    version=get_version_string(),
    description='Plasma Finance SDK',
    long_description=readme,
    long_description_content_type='text/markdown',
    author=get_author_string(),
    author_email='zhaolantao1995@163.com',
    url='https://www.ultrastiching.com/home',
    keywords=['python', 'finance', 'sdk','api'],
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
      'Programming Language :: Python :: 3.11',
    ]
)