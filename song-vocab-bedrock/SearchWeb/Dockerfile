# Use the AWS Lambda Python 3.13 base image 
FROM public.ecr.aws/lambda/python:3.13

# Set the working directory
WORKDIR /var/task

# Copy function code into container
COPY search_web.py .

# Install dependencies directly in the container
RUN pip install --no-cache-dir duckduckgo-search -t .

# Command to start the Lambda function
CMD ["search_web.lambda_handler"]
