FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
COPY ssl_ke.pem certs/thegagali.pem
COPY ssl_privat_ke.pem certs/thegagali-key.pem
EXPOSE 443 80