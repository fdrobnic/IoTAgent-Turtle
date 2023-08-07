FROM  python:3.9-alpine@sha256:e80214a705236091ee3821a7e512e80bd3337b50a95392a36b9a40b8fc0ea183  as  build

LABEL "maintainer"="FIWARE Foundation e.V."
LABEL "description"="An Internet of Things Agent for the RDF DataQube Turtle format. This IoT Agent is designed to be a bridge between ISOXML/ADAPT and the ETSI NGSI-LD interface of a FIWARE Context Broker."
LABEL "name"="iotagent-turtle"
LABEL "summary"="IoT Agent for the DataQube representation in RDF Turtle format used in statistical environments"

LABEL "org.opencontainers.image.authors"="fernando.lopez@fiware.org"
LABEL "org.opencontainers.image.documentation"=""
LABEL "org.opencontainers.image.vendor"="FIWARE Foundation e.V."
LABEL "org.opencontainers.image.licenses"="Apache2.0"
LABEL "org.opencontainers.image.title"="iotagent-turtle"
LABEL "org.opencontainers.image.description"="An Internet of Things Agent for the RDF DataQube Turtle format. This IoT Agent is designed to be a bridge between ISOXML/ADAPT and the ETSI NGSI-LD interface of a FIWARE Context Broker."
LABEL "org.opencontainers.image.source"="https://github.com/flopezag/IoTAgent-Turtle"
LABEL "org.opencontainers.image.version"="0.1.0"
LABEL "org.python.version"="python:3.9"

RUN  apk  update
# RUN apt-get install -y --no-install-recommends \
# 	build-essential gcc

WORKDIR  /usr/app
RUN  python  -m  venv  /usr/app/venv
ENV  PATH="/usr/app/venv/bin:$PATH"

COPY  requirements.txt  .
RUN  pip  install  --no-cache-dir  --upgrade  -r  requirements.txt

FROM python:3.9-alpine@sha256:e80214a705236091ee3821a7e512e80bd3337b50a95392a36b9a40b8fc0ea183

ENV PORT=${IOTA_PORT:-5000}

LABEL "maintainer"="FIWARE Foundation e.V."
LABEL "description"="An Internet of Things Agent for the RDF DataQube Turtle format. This IoT Agent is designed to be a bridge between ISOXML/ADAPT and the ETSI NGSI-LD interface of a FIWARE Context Broker."
LABEL "name"="iotagent-turtle"
LABEL "summary"="IoT Agent for the DataQube representation in RDF Turtle format used in statistical environments"

LABEL "org.opencontainers.image.authors"="fernando.lopez@fiware.org"
LABEL "org.opencontainers.image.documentation"=""
LABEL "org.opencontainers.image.vendor"="FIWARE Foundation e.V."
LABEL "org.opencontainers.image.licenses"="Apache2.0"
LABEL "org.opencontainers.image.title"="iotagent-turtle"
LABEL "org.opencontainers.image.description"="An Internet of Things Agent for the RDF DataQube Turtle format. This IoT Agent is designed to be a bridge between ISOXML/ADAPT and the ETSI NGSI-LD interface of a FIWARE Context Broker."
LABEL "org.opencontainers.image.source"="https://github.com/flopezag/IoTAgent-Turtle"
LABEL "org.opencontainers.image.version"="0.1.0"
LABEL "org.python.version"="python:3.9"

RUN  addgroup  -g  99  python  &&  \
     adduser   -S  -u  999  -g  python  python

RUN  mkdir  /usr/app  &&  chown  python:python  /usr/app
WORKDIR  /usr/app

COPY  --chown=python:python  --from=build  /usr/app/venv  ./venv
COPY  --chown=python:python  .  .

USER 999

ENV PATH="/usr/app/venv/bin:$PATH"
CMD ["python", "agent.py", "server", "--host", "0.0.0.0", "--port", "5000"]
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD curl -f https://localhost:${PORT}/version

EXPOSE ${PORT}
