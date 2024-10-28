FROM python:3.12

WORKDIR /app

COPY docs/docs_src/getting_started/nats_n_fastapi/main_1_nats.py /app/main_1_nats.py
COPY docs/docs_src/getting_started/nats_n_fastapi/main_2_fastapi.py /app/main_2_fastapi.py
COPY docs/docs_src/getting_started/nats_n_fastapi/main_3_mesop.py /app/main_3_mesop.py

RUN pip install fastagency[autogen,mesop,server,fastapi,nats]

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app

USER appuser

EXPOSE 8000 8008 8888

COPY docs/docs_src/getting_started/docker/nats_fastapi_mesop/run_fastagency.sh /app/run_fastagency.sh

CMD ["/app/run_fastagency.sh"]

# Run the build command from root of fastagency repo
# docker build -t deploy_nats_fastapi_mesop -f docs/docs_src/getting_started/docker/nats_fastapi_mesop/nats_fastapi_mesop.Dockerfile .

# Run the container
# NATS docker container should be running already
# docker run --rm -d --name deploy_nats_fastapi_mesop -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8000:8000 -p 8008:8008 -p 8888:8888 --network=host deploy_nats_fastapi_mesop
