from setuptools import setup, find_packages

setup(
    name='file_text_extractor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF',
        'python-docx',
        'google-cloud-storage'
    ],
    author='Sanjana Jain',
    author_email='sanjana.jain@skillsbridge.ai',
    description='A package to extract text from various file formats including PDF and DOCX.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)