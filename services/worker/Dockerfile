FROM python:3.12-alpine3.24

# copy the program files to the container
WORKDIR /app

COPY . /app

RUN <<EOF 
python -m pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt
EOF

#Create a system user: worker and give permissions to the /app directory
RUN <<EOF 
addgroup -S worker && adduser -S worker -G worker
chown -R worker:worker /app
EOF

USER worker

HEALTHCHECK --interval=10s --timeout=10s --start-period=5s --start-interval=1s \
 CMD python3 /app/worker_healthcheck.py || exit 1


CMD ["python3", "worker.py"]