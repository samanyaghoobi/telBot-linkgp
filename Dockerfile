FROM python:3.9.19-slim

# Set timezone to Tehran
ENV TZ=Asia/Tehran
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create log directory and set working dir
RUN mkdir -p /logs
WORKDIR /bot

# Install requirements without copying source code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy logrotate config (optional)
COPY logrotate.conf /etc/logrotate.d/bot-logrotate.conf

# Run main.py from mounted code
CMD ["python", "main.py"]
