from python:3.10-alpine

EXPOSE 8014/tcp

ARG PROJECT_DIR=/recommendation_service
ENV PROJECT_DIR=/recommendation_service
ENV PYTHONPATH=/

WORKDIR $PROJECT_DIR

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -h "$PROJECT_DIR"

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x entrypoint.sh; chown -R appuser:appgroup "$PROJECT_DIR"
USER appuser

ENTRYPOINT ["sh", "entrypoint.sh"]