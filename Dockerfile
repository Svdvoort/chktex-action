FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
  chktex


WORKDIR /root

COPY \
  entrypoint.sh \
  /root/

ENTRYPOINT ["/root/entrypoint.sh"]
