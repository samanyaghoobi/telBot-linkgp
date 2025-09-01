FROM python:3.9.19-slim

# Set timezone to Tehran
ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Improve Python behavior in containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create app user and directories
RUN useradd -ms /bin/bash appuser
RUN mkdir -p /logs /bot && chown -R appuser:appuser /logs /bot

WORKDIR /bot

# Copy requirements first to leverage layer cache
COPY --chown=appuser:appuser requirements.txt /bot/requirements.txt
RUN pip install -r requirements.txt

# Copy source code
COPY --chown=appuser:appuser . /bot

# NOTE: We persist logs via volume /logs; rotate on host via logging options or external tools.
# COPY logrotate.conf /etc/logrotate.d/bot-logrotate.conf  # Not recommended inside the container

USER appuser

CMD ["python", "main.py"]
