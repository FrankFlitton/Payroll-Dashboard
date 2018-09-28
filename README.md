# App Structure

## Overview
The app is made of 3 Docker containers, `frontend`, `backend` and `db`. The is built with by vuejs, the backend by Django Rest Framework, and db is a postgress container.

## Setup Instructions with Docker
This has been tested using the latest Docker for OSX.

### Start the images

$ ```docker-compose up```

That's it. This is a great time to grab a coffee. ☕️

If there are no built images, docker will create and run them. The app servers can be accessed at the following addresses:

```
    Frontend:   http://localhost:8080
    Server:     http://localhost:8000
```

### Accessing Django Admin Panel

Run $ ``` docker ps ``` to get a list of live images.

Find the `backend` container name in the `NAMES` column, last column in the table. Enter the backend image using this pattern:

$ ```docker exec -ti {IMAGE_NAME} /bin/bash```

You can now use the Linux console to run commands. Run the following to create your admin account.

$ ```python ./manage.py createsuperuser```

You can now log in at `http://localhost:8000/admin`.
