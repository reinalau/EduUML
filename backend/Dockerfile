FROM public.ecr.aws/lambda/python:3.12

# Install git and other system dependencies
RUN yum update -y && \
    yum install -y git && \
    yum clean all

# Copy requirements and install Python dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy function code
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Set the CMD to your handler
CMD ["src.handlers.main_handler.lambda_handler"]