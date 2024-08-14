FROM python:3.9.19-slim 

# make dir
WORKDIR /bot

# copy alla file to dir '/bot'
COPY . .

# install requrment 
RUN pip install --no-cache-dir -r requirements.txt

#run code
CMD ["python", "main.py"]