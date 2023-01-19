FROM python:3.9.16-bullseye
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m spacy download en_core_web_sm
CMD ["python", "app.py"]
