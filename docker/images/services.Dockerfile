FROM python:3.10.15-alpine3.20 as base
RUN apk update && apk add git bash libmagic gcc libc-dev
RUN python -m pip install --upgrade pip==23.3
RUN adduser xformer -D
ENV ASSETS_DIR=/app/controlplane/src/assets
ENV ACE_TEMP_DIR=/temp_ace/
RUN mkdir ${ACE_TEMP_DIR} && cd ${ACE_TEMP_DIR} && git clone -b v1.5.0 https://github.com/ajaxorg/ace-builds.git
RUN mkdir /app
RUN chown xformer /app
COPY controlplane/ /app/controlplane/
RUN rm -fr /app/controlplane/src/assets/src-*
COPY dataplane/ /app/dataplane/
COPY modules/ /app/modules/
COPY requirements.txt /app/
COPY lib/ /app/lib/
COPY start-prod-controlplane.sh /app/
COPY start-prod-dataplane.sh /app/
COPY start-service.sh /app/
ENV ACE_SRC=src-min
RUN mkdir -p ${ASSETS_DIR}/${ACE_SRC}/snippets
RUN cp -r ${ACE_TEMP_DIR}ace-builds/${ACE_SRC}/snippets/python.js ${ASSETS_DIR}/${ACE_SRC}/snippets/.
RUN cp ${ACE_TEMP_DIR}ace-builds/${ACE_SRC}/*.js ${ASSETS_DIR}/${ACE_SRC}/.
RUN rm ${ASSETS_DIR}/${ACE_SRC}/mode-*
RUN rm ${ASSETS_DIR}/${ACE_SRC}/theme-*
RUN rm ${ASSETS_DIR}/${ACE_SRC}/worker-*
RUN cp ${ACE_TEMP_DIR}ace-builds/${ACE_SRC}/mode-python.js ${ASSETS_DIR}/${ACE_SRC}/.
RUN cp ${ACE_TEMP_DIR}ace-builds/${ACE_SRC}/theme-monokai.js ${ASSETS_DIR}/${ACE_SRC}/.
RUN rm -rf ${ACE_TEMP_DIR}
RUN chown -R xformer /app
WORKDIR /app

FROM base as pinst
RUN pip install --no-cache-dir -r /app/requirements.txt

FROM pinst
RUN apk del gcc libc-dev
USER xformer
WORKDIR /app
ENV PYTHONPATH=/app
ENTRYPOINT [ "/app/start-service.sh" ]
