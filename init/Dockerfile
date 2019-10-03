FROM alpine:3.8
RUN apk add mariadb-client
ADD wait_for_mysql.sh .
RUN chmod 777 wait_for_mysql.sh
USER 1001
CMD ["/bin/sh", "-c", "/wait_for_mysql.sh"]