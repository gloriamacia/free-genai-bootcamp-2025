# Use AWS Lambda Python 3.13 base image for x86_64
FROM public.ecr.aws/lambda/python:3.13

# Set the working directory
WORKDIR /var/task

# Copy function code into container
COPY extract_vocabulary.py .

# Install required dependencies (NLTK for stopword filtering)
RUN pip install --no-cache-dir nltk -t .

# Ensure stopwords are downloaded in the container
RUN python -c "import nltk; nltk.download('stopwords')"

# Command to start the Lambda function
CMD ["extract_vocabulary.lambda_handler"]
