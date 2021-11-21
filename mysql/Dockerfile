FROM mysql:8.0.27
RUN groupadd -g 1000 mysql_user
RUN useradd mysql_user --uid 1000 -g 1000
RUN chown -R mysql_user:mysql_user /var/lib/mysql
USER mysql_user
COPY ./init.sql /docker-entrypoint-initdb.d/
