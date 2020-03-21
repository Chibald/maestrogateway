FROM python:3.7-alpine

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt && rm requirements.txt

COPY ./*.py ./maestro/

ENTRYPOINT [ "python3", "/maestro/maestro.py" ]
