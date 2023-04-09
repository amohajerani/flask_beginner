FROM nginx
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/
COPY ssl_ke.pem certs/thegagali.pem
COPY ssl_private_ke.pem certs/thegagali-key.pem