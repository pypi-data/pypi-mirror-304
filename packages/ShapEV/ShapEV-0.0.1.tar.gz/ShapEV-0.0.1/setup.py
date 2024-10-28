from setuptools import setup, find_packages

setup(
    name='ShapEV',
    version='0.0.1',
    description="A package for identifying Equivalent Value based on joint SHAP values",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  # Specify the format of long_description
    include_package_data=True,
    author='Cao Bin',  # Added space between first and last name for clarity
    author_email='bcao@shu.edu.com',
    maintainer='Cao Bin',  # Added space between first and last name for clarity
    maintainer_email='binjacobcao@gmail.com',
    license='MIT',  # Simplified license specification
    url='https://github.com/Bin-Cao/ShapEV',
    packages=find_packages(),  # Automatically include all Python modules
    package_data={'': ['*.txt', '*.md']},  # Specify non-Python files to include (e.g., .txt and .md files)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.5',
    install_requires=[
        'scikit-learn',
    ],
    entry_points={
        'console_scripts': [
            'shap_ev = ShapEV:main',  # Add an appropriate entry point (you'll need to define main in your package)
        ],
    },
)
