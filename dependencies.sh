#/bin/bash

apt-get -y install python-dev libxml2-dev libxslt1-dev antiword unrtf poppler-utils pstotext tesseract-ocr
apt-get -y install flac ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig libpulse-dev
apt-get -y install python3-pip
pip3 install textract

pip3 install pytesseract
pip3 install pdf2image
pip3 install PyMuPDF Pillow
sudo apt-get install tesseract-ocr
