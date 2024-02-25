# Use the official Python image
FROM python:3.9-slim

EXPOSE 8000

WORKDIR /app
#COPY . /app
COPY . .

# Install pip requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app:app"]