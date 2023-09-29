FROM python:3.8

WORKDIR /usr

COPY ./requirements.txt /usr/requirements.txt
COPY ./main.py /usr
COPY ./modelos /usr/modelos

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]
CMD [ "main.py" ]