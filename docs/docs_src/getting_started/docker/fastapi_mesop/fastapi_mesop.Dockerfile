FROM python:3.12

WORKDIR /app

COPY docs/docs_src/getting_started/fastapi/main_1_fastapi.py /app/main_1_fastapi.py
COPY docs/docs_src/getting_started/fastapi/main_2_mesop.py /app/main_2_mesop.py

RUN pip install fastagency[autogen,mesop,server,fastapi]

EXPOSE 8000

COPY docs/docs_src/getting_started/docker/fastapi_mesop/run_fastagency.sh /app/run_fastagency.sh

CMD ["/app/run_fastagency.sh"]

# Run the build command from root of fastagency repo
# docker build -t deploy_fastapi_mesop -f docs/docs_src/getting_started/docker/fastapi_mesop/fastapi_mesop.Dockerfile .
# docker run --rm -d --name deploy_fastapi_mesop -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8008:8008 -p 8888:8888 deploy_fastapi_mesop
