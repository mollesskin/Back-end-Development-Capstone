FROM python:3.9.16-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 APP=/app
WORKDIR $APP
COPY requirements.txt $APP
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . $APP
EXPOSE 8000
RUN chmod +x /app/entrypoint.sh && chmod -R g=u /app
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]
