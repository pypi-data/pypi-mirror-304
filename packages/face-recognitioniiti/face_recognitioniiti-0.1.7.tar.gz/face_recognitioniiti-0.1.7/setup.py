from setuptools import setup, find_packages

setup(
    name='face_recognitioniiti',
    version='0.1.7',  # Update as needed
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
        "torch",
        "protobuf",
        "opencv-python",
        "torchvision",
        "ultralytics",
        "arcFace",  # Ensure ArcFace can be installed via pip
    ],
    extras_require={
        'dev': [
            # Development dependencies can go here
        ],
    },
      entry_points={
        "console_scripts": [
            "face-recognition=face_recognition_system.face_recognition_system:main",
        ],
    },
    author='Yatharth Gupta',
    author_email='kkmvymayank@gmail.com',
    description='A package that contains a Real-time Face Recognition System.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Warlord-K/InterIIT-facerecognition',  # Update with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
