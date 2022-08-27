# Image
FROM python:3-slim
LABEL maintainer="David Pinhas <davepinhas89@gmail.com>"

# Install CryptoView
RUN mkdir -p /deploy/app
COPY gunicorn_config.py /deploy/gunicorn_config.py

# Create Work Directory
COPY . /deploy/app
WORKDIR /deploy/app

# Configure Python
RUN python3 -m venv venv
ENV PATH=venv/bin:$PATH
RUN . venv/bin/activate
RUN venv/bin/pip3 install -r /deploy/app/requirements.txt

# Ports
EXPOSE 5001

# Run Command
CMD ["venv/bin/gunicorn", "--config", "/deploy/gunicorn_config.py", "wsgi:app"]