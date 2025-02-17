FROM python:3.13

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app
# Set the working directory
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# Install dependencies
COPY ./requirements .
RUN pip install --no-cache-dir -r ${BUILD_ENVIRONMENT}.txt

# Copy the project files
# COPY . /app/

COPY ./docker/local/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# USER 1000
CMD ["/entrypoint.sh"]
# COPY ./docker/local/entrypoint.sh /entrypoint
# RUN sed -i 's/\r$//g' /entrypoint
# RUN chmod +x /entrypoint
# CMD ["/entrypoint.sh"]