from setuptools import setup, find_packages

setup(
    name="SSUphysicsTools",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "pandas"
    ],
    author="Taeyoung Kim",
    author_email="rocketman@soongsil.ac.kr",
    description="숭실대학교 물리학과 실험에 사용되는 데이터 처리 및 시각화 도구",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/kty1004/SSUphysicsExperiment_Supporting_tools?tab=readme-ov-file#readme",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.13.0',
)