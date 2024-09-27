FROM python:3.10.15-alpine3.20 as base
RUN apk update && apk add git bash libmagic
RUN python -m pip install --upgrade pip==23.3
RUN adduser xformer -D
ENV ASSETS_DIR=/app/controlplane/src/assets
ENV ACE_TEMP_DIR=/temp_ace/
RUN mkdir ${ACE_TEMP_DIR} && cd ${ACE_TEMP_DIR} && git clone -b v1.5.0 https://github.com/ajaxorg/ace-builds.git 
RUN mkdir /app
RUN chown xformer /app
COPY controlplane/ /app/controlplane/
COPY dataplane/ /app/dataplane/
COPY modules/ /app/modules/
COPY requirements.txt /app/
COPY lib/ /app/lib/
COPY start-prod-controlplane.sh /app/
COPY start-prod-dataplane.sh /app/
COPY start-service.sh /app/
RUN mkdir -p ${ASSETS_DIR}/src-noconflict/snippets
RUN cp -r ${ACE_TEMP_DIR}ace-builds/src-noconflict/snippets/python.js ${ASSETS_DIR}/src-noconflict/snippets/. 
RUN cp ${ACE_TEMP_DIR}ace-builds/src-noconflict/*.js ${ASSETS_DIR}/src-noconflict/. 
RUN rm ${ASSETS_DIR}/src-noconflict/mode-*
RUN rm ${ASSETS_DIR}/src-noconflict/worker-*
RUN cp ${ACE_TEMP_DIR}ace-builds/src-noconflict/mode-python.js ${ASSETS_DIR}/src-noconflict/. 
RUN rm -rf ${ACE_TEMP_DIR}
RUN chown -R xformer /app
WORKDIR /app
RUN pip install --no-cache-dir -r /app/requirements.txt 

FROM base 
USER xformer
WORKDIR /app
ENV PYTHONPATH=/app
ENTRYPOINT [ "/app/start-service.sh" ]


