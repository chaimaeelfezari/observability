FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests
COPY discord_proxy.py .
CMD ["python", "discord_proxy.py"]