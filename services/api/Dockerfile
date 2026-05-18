FROM python:3.12-slim 

WORKDIR /app

COPY . /app

#create a virtual env
RUN python3 -m venv .venv

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN pip install -r requirements.txt

#Create a system user: worker
RUN  groupadd -r worker && useradd -r -g worker worker

RUN chown -R worker:worker /app

USER worker

HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --start-interval=1s \
 CMD python3 /app/api_healthcheck.py || exit 1


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
