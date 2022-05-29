FROM 395499912268.dkr.ecr.eu-west-1.amazonaws.com/beehive-extractor-base
USER root
ENV HOME /opt/docker
ENV SERVING_API ALL
WORKDIR ${HOME}


# install python dependencies
COPY requirements.txt ${HOME}/requirements.txt
COPY get_dependencies.py ${HOME}/get_dependencies.py

RUN export CODEARTIFACT_AUTH_TOKEN=`aws codeartifact get-authorization-token --domain vatbox --domain-owner 395499912268 --query authorizationToken --output text` && \
    python3 -m pip config set global.index-url https://pypi.python.org/simple && \
    python3 -m pip config set global.extra-index-url https://aws:$CODEARTIFACT_AUTH_TOKEN@vatbox-395499912268.d.codeartifact.eu-west-1.amazonaws.com/pypi/vatbox-py/simple/

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install --upgrade beehive-infra==PLACEHOLDER
RUN python3 ${HOME}/get_dependencies.py

# copy extractor
COPY extractor /opt/docker/extractor
COPY start_extractor.sh /opt/docker/start_extractor.sh

# Set up user and default entrypoint
RUN chown -R daemon:daemon /opt/docker
USER daemon
RUN chmod +x /opt/docker/*.sh
WORKDIR /opt/docker
ENTRYPOINT tail -f /dev/null
EXPOSE 80

ENV AWS_ACCESS_KEY_ID=
ENV AWS_SECRET_ACCESS_KEY=
ENV AWS_DEFAULT_REGION=

