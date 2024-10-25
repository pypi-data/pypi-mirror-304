from setuptools import setup, find_packages

# อ่านไฟล์ README.md ด้วย UTF-8 encoding
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="voice_recorder",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyaudio>=0.2.11",
        "numpy>=1.19.0",
        "scipy>=1.5.0",
        "matplotlib>=3.3.0",
        "keyboard>=0.13.5"
    ],
    license="MIT",
    author="Pakon",
    author_email="okpkmyang12@gmail.com",
    description="A high-quality audio recorder with voice detection",
    long_description=long_description,  # ใช้ตัวแปรที่อ่านมาแทน
    long_description_content_type="text/markdown",
    url="https://github.com/Pakon12/voice_recorder_V1.0.0",
    download_url="https://github.com/Pakon12/voice_recorder_V1.0.0/archive/v1.0.0.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)