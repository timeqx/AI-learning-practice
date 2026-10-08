FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY data ./data
EXPOSE 8000
# Educational local demonstration only; do not expose without authentication and hardening.
CMD ["uvicorn", "hmo_lab.api:app", "--host", "0.0.0.0", "--port", "8000"]
