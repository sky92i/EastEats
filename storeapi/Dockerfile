FROM python:3

# Set the working directory to /EasyEats in the container
WORKDIR /EasyEats

# Copy the current directory contents into the container at /EasyEats
COPY . /EasyEats

#install dependencies
RUN python3 -m pip install --user --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python","app.py"]