FROM python


EXPOSE 5000
EXPOSE 8000

COPY . ./service
WORKDIR /service

RUN apt-get update


RUN export PYTHONPATH=$PWD
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]