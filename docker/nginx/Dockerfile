FROM jwilder/nginx-proxy
RUN rm /etc/nginx/sites-enabled/default
ADD sites-enabled/ /etc/nginx/sites-enabled
ADD medna.pem /etc/medna.pem