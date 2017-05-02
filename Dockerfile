FROM python:3.5
MAINTAINER Ricardo Tercero <ricardo.tercero@vordem.mx>

# environment configuration
ENV PYTHONUNBUFFERED 1

# create app directory
WORKDIR /root

# install pip requirements
ADD requirements.txt /root/

# install pip requirements
RUN pip install -r requirements.txt --default-timeout 450

# run code through volume
VOLUME /usr/src/app
WORKDIR /usr/src/app

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "fronesis.wsgi:application", "--reload", "--enable-stdio-inheritance"]
