FROM python:3.7-alpine as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apk add --no-cache gcc git musl-dev

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN set -eux; adduser -u 82 -D -S -G www-data www-data
RUN set -eux; mkdir -p /app; chown www-data:www-data /app;
USER www-data
WORKDIR /app

EXPOSE 80

# Run the application
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:80", "main:app"]