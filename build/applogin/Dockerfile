FROM python:3.10.13-alpine3.18 AS local

ENV UID 1000
ENV GID 1000
ENV PYTHONPATH "/home/applogin/applogin"

COPY run_container.sh /
RUN chmod +x /run_container.sh

RUN addgroup -g $GID applogin
RUN adduser -G applogin -u $UID -D applogin

VOLUME /home/applogin
ENV PATH="$PATH:/home/applogin/.local/bin/"
RUN echo $PATH

USER applogin

ENTRYPOINT ["/run_container.sh"]
CMD /home/applogin

