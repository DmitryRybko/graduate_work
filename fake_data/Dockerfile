FROM python:3.10-alpine

ARG PROJECT_DIR=/project
ENV PYTHONPATH=/project
ENV PROJECT_DIR=/project

WORKDIR "$PROJECT_DIR"

# Create a group and user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup -h "$PROJECT_DIR"

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appgroup "$PROJECT_DIR";
USER appuser

ENTRYPOINT ["sh", "src/entrypoint.sh"]