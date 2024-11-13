FROM python:3.12

WORKDIR /app

# Install nginx
RUN apt-get update && apt-get install -y --no-install-recommends nginx gettext \
    && rm -rf /var/lib/apt/lists/*

COPY my_fastagency_app /app/my_fastagency_app

COPY pyproject.toml README.md /app/
COPY docker/content/* /app/


RUN pip install --upgrade pip && pip install --no-cache-dir -e "."

# Add user appuser with root permissions
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser /app \
    && chown -R appuser:appuser /etc/nginx/conf.d /var/log/nginx /var/lib/nginx \
    && touch /run/nginx.pid && chown -R appuser:appuser /run/nginx.pid \
    # Allow binding to ports > 1024 without root
    && sed -i 's/listen 80/listen 9999/g' /etc/nginx/sites-available/default \
    && sed -i 's/listen \[::\]:80/listen \[::\]:9999/g' /etc/nginx/sites-available/default \
    # Create required directories with correct permissions
    && mkdir -p /var/cache/nginx /var/run \
    && chown -R appuser:appuser /var/cache/nginx /var/run

USER appuser

# ToDo: Fix exposing ports
# EXPOSE 8000 8008 8888

CMD ["/app/run_fastagency.sh"]

# Run the build command from root of fastagency repo
# docker build -t deploy_fastagency -f docker/Dockerfile .

# Run the container

# NATS docker container should be running already

# docker run --rm -d --name deploy_fastagency -e OPENAI_API_KEY=$OPENAI_API_KEY -e NATS_URL=$NATS_URL -e FASTAGENCY_NATS_PASSWORD=$FASTAGENCY_NATS_PASSWORD -p 8000:8000 -p 8008:8008 -p 8888:8888 --network=host deploy_fastagency
