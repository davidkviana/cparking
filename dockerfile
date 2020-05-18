FROM python:3.7-slim

WORKDIR "/parkcontrol"
COPY Pipfile Pipfile.lock ./

RUN pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --ignore-pipfile --system

COPY ./ ./
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]