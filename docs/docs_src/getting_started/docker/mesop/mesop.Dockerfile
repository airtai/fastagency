FROM python:3.12

WORKDIR /app

COPY docs/docs_src/getting_started/main_mesop.py /app/main_mesop.py

RUN pip install fastagency[autogen,mesop,server]

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app

USER appuser

EXPOSE 8000

COPY docs/docs_src/getting_started/docker/mesop/run_fastagency.sh /app/run_fastagency.sh

CMD ["/app/run_fastagency.sh"]

# Run the build command from root of fastagency repo
# docker build -t deploy_mesop -f docs/docs_src/getting_started/docker/mesop/mesop.Dockerfile .
# docker run --rm -d --name deploy_mesop -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8000:8000 deploy_mesop
