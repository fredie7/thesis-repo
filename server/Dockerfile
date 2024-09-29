# Start from Python base image
FROM python:3.10

# Change working directory
WORKDIR /code

# Add requirements file to image
COPY ./requirements.txt /code/requirements.txt
COPY ./annotated_data.csv /code/annotated_data.csv
COPY .env /code/.env

# Install Python libraries
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Add Python code
COPY ./app/ /code/app/

# Specify default command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
