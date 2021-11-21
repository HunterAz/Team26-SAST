FROM nginx:latest

COPY ./certs/meok.sitict.net.key /etc/nginx/certs/meok.sitict.net.key
COPY ./certs/meok.sitict.net.crt /etc/nginx/certs/meok.sitict.net.crt
COPY ./certs/isrg-root-x1-cross-signed.pem /etc/nginx/certs/isrg-root-x1-cross-signed.pem
COPY ./certs/dhparam.pem /etc/nginx/certs/dhparam.pem
COPY ./conf/default.conf /etc/nginx/conf.d/default.conf

RUN groupmod -g 1000 nginx
RUN usermod -u 1000 -g 1000 nginx

RUN chown -R nginx:nginx /var/cache/nginx && \
        chown -R nginx:nginx /var/log/nginx && \
        chown -R nginx:nginx /etc/nginx/conf.d && \
        chown -R nginx:nginx /etc/nginx/certs

RUN touch /var/run/nginx.pid && \
        chown -R nginx:nginx /var/run/nginx.pid

USER nginx
