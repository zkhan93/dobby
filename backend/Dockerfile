FROM python:3.8-slim

WORKDIR /app
COPY app/requirements.txt .
RUN pip install -r requirements.txt

COPY app .
EXPOSE 5000

# ENV FLASK_APP=run
# ENV FLASK_ENV=development
# ENV FLASK_RUN_HOST=0.0.0.0
# ENV FLASK_RUN_PORT=5000
# CMD [ "flask", "run"]

CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "run:app"]`