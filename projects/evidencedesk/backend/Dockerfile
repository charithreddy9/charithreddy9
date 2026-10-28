FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app DATA_DB_PATH=/app/data/evidencedesk.sqlite3
WORKDIR /app
COPY backend/requirements*.txt /app/backend/
ARG INSTALL_SEMANTIC=false
RUN if [ "$INSTALL_SEMANTIC" = "true" ]; then \
      pip install --no-cache-dir -r backend/requirements-semantic.txt; \
    else pip install --no-cache-dir -r backend/requirements.txt; fi
COPY backend /app/backend
RUN useradd --system --uid 10001 --create-home appuser && mkdir -p /app/data /home/appuser/.cache && chown -R appuser:appuser /app/data /home/appuser
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=45s --retries=3 CMD python -c "import urllib.request;urllib.request.urlopen('http://127.0.0.1:8000/api/health',timeout=4)"
CMD ["uvicorn","backend.app:app","--host","0.0.0.0","--port","8000","--workers","1","--proxy-headers"]
