from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    description = f.read()

setup(
    name='smretrofit',
    version='1.0.4',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'requests',
        'Pillow',
        'numpy',
        # 'cryptography'
    ],
    long_description=description,
    long_description_content_type='text/markdown',
    keywords='computer vision requests image and video processing',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
    ],
    license='Somikoron License',
    url='https://www.somikoron.ai',
    author='Somikoron',
    author_email='contact@somikoron.ai',
    python_requires='>=3.7',
    project_urls={
        'Documentation': 'https://api.somikoron.ai',
        'Source': 'https://github.com/somikoronAI-Source/smretrofit.git',
        'Bug Tracker': 'https://github.com/somikoronAI-Source/smretrofit/issues/1',
    },
)
