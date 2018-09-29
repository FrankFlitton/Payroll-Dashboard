# Overview

The app is composed of 3 Docker containers, `frontend`, `backend` and `db`. The frontend is built with by vuejs, the backend by Django Rest Framework, and the db is postgress.

# Highlights

I'm proud of the scalablity of the solution and the responsive design. UX was a key consideration of how I approached the problem. The data model can be easily extended to contain relevant paycheque details such as employee names, tax deductions, or csv provider. With some slight adjustments, the app could be deployed to a production server.

The highlights of the app include:
- Responsive frontend, styled with subtle animations
- Data is clearly presented, invites the user to sort table
- Network of Docker containers seperated by system
- Clear error messages incorperated into the interface
- Data model can be easily extended
- Admin panel for debugging data and APIs
- CSV file is never stored, only read (security)
- Branding colours sampled from Wave's website

# Setup Instructions with Docker
This has been tested using the latest Docker for OSX.

## Start the images

$ ```docker-compose up```

That's it. This is a great time to grab a coffee. ☕️

If there are no built images, docker will create and run them. The app servers can be accessed at the following addresses:

```
    Frontend:   http://localhost:8080
    Server:     http://localhost:8000
```

## Accessing Django Admin Panel

Run $ ``` docker ps ``` to get a list of live images.

Find the `backend` container name in the `NAMES` column, last column in the table. Enter the backend image using this pattern:

$ ```docker exec -ti {IMAGE_NAME} /bin/bash```

You can now use the Linux console to run commands. Run the following to create your admin account.

$ ```python ./manage.py createsuperuser```

You can now log in at `http://localhost:8000/admin`.
