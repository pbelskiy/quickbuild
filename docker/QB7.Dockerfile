FROM openjdk:8
RUN apt-get update && apt-get install -y wget
RUN wget 'https://build.pmease.com/download/4555/artifacts/quickbuild-7.0.32.tar.gz' -O quickbuild.tar && tar -zxvf quickbuild.tar -C /opt
EXPOSE 8810
ENTRYPOINT /opt/quickbuild-7.0.32/bin/server.sh console
