FROM python:3.9

ADD src ./src
ADD golemio-api.cert .
ADD config.yaml .
ENV PYTHONPATH "${PYTHONPATH}:/src/common"

RUN pip install pyyaml requests

#CMD ["python", "./src/common/common.py"]
CMD ["python", "./src/wfloaddata/loadstops.py"]