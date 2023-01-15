FROM python:3.10

WORKDIR /var/www/services

COPY ./requirements/common.txt /var/www/services/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /var/www/services/requirements.txt

EXPOSE 8000

COPY . /var/www/services/

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--workers", "1", "--port", "8000"]
