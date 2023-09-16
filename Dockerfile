# 基本となるイメージを指定
FROM ubuntu:20.04

# 必要なパッケージをインストール
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:alex-p/tesseract-ocr && \
    apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev && \
    apt-get install -y tesseract-ocr-jpn tesseract-ocr-jpn-vert && \
    apt-get install -y tesseract-ocr-script-jpan tesseract-ocr-script-jpan-vert

# Pythonをインストール
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# アプリケーションのコードと依存関係をコピー
COPY . /app
WORKDIR /app

# Python依存関係をインストール
RUN pip3 install -r requirements.txt

# エントリーポイントを設定
CMD ["python3", "get_ocr.py"]
