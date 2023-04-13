#Parent image is build from ./docker/dockerfile
FROM bdh-parent

ADD src ./src
ADD golemio-api.cert .
ADD config.yaml .
ENV PYTHONPATH "${PYTHONPATH}:/src/common"

#CMD ["python", "./src/common/common.py"]
#CMD ["python", "./src/wfloaddata/loadstops.py"]
#CMD ["python", "./src/wfloaddata/loaddelay.py"]
CMD ["python", "./src/wfloaddata/runworkflow.py"]