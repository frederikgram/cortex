FROM python


EXPOSE 5000
EXPOSE 8000

COPY . ./service
WORKDIR /service

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y


RUN export PYTHONPATH=$PWD
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]