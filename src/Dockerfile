FROM tiangolo/uwsgi-nginx:python3.11
COPY ./api /api
WORKDIR /api
ENV UWSGI_INI ./CyCarrier/uwsgi.ini
COPY entrypoint.sh /entrypoint.sh

RUN pip3 install -r requirements.txt

ENTRYPOINT ["sh", "/entrypoint.sh"]
EXPOSE 8001