# Pull base image
FROM python:3.7
# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code/
# Install dependencies
COPY . /code/
RUN pip install -r req.txt
EXPOSE 8000
CMD ["python", "main.py"]