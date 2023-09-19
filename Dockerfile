FROM python:3.11-alpine	
RUN /usr/local/bin/python -m pip install --upgrade pip
ADD ./requirements.txt /
RUN pip install -r requirements.txt
WORKDIR src
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8088"]
