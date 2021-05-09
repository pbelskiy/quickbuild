FROM openjdk:8
RUN apt-get update && apt-get install -y wget
RUN wget 'https://www.pmease.com/artifacts/5299/quickbuild-10.0.34.tar.gz' -O quickbuild.tar && tar -zxvf quickbuild.tar -C /opt
EXPOSE 8810
ENTRYPOINT /opt/quickbuild-10.0.34/bin/server.sh console
