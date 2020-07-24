FROM        tensorflow/tensorflow:2.2.0rc0-gpu-py3
COPY       	./requirements.txt /app/requirements.txt
WORKDIR    	/app
RUN         pip install --upgrade pip
RUN 		pip install -r requirements.txt
RUN         pip list
COPY       	. /app
WORKDIR    	/app

# openshift set permission to non-root users for /app directory
RUN chgrp -R 0 /app && \
    chmod -R g=u /app

# openshift set running user 
USER 1001

ENTRYPOINT 	["python"]
CMD 		["startup.py"]