FROM python:3.12-alpine3.24

# copy the program files to the container
WORKDIR /app

COPY . /app

RUN <<EOF
python -m pip install --no-cache-dir --upgrade pip
pip install --no-cache-dir -r requirements.txt
EOF

#Create a system user: api and give permissions to the /app directory
RUN <<EOF
addgroup -S api && adduser -S api -G api
chown -R api:api /app
EOF

RUN apk add --no-cache curl  

USER api

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --start-interval=1s \
 CMD python3 /app/healthcheck.sh || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
