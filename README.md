# Simple Payroll Batch
> A Simple VueJS, Django, and Docker solution

## Project Description

A simple web app to to determine how much each employee should be paid in each
_pay period_.

## Project Scenario

This app assumes the company only pays its employees by the hour (there are no
salaried employees.) Employees belong to one of two _job groups_ which
determine their wages; job group A is paid $20/hr, and job group B is paid
$30/hr. Each employee is identified by a string called an "employee id" that is
globally unique in their system.

Hours are tracked per employee, per day in comma-separated value files (CSV).
Each individual CSV file is known as a "time report", and will contain:

1. A header, denoting the columns in the sheet (`date`, `hours worked`,
   `employee id`, `job group`)
1. 0 or more data rows
1. A footer row where the first cell contains the string `report id`, and the
   second cell contains a unique identifier for this report.

### Assumptions

1. Columns will always be in that order.
1. There will always be data in each column.
1. There will always be a well-formed header line.
1. There will always be a well-formed footer line.

An example input file named `sample.csv` is included in this repo.

### How the application works

1. The app accepts (via a form) a CSV file with the schema
   described in the previous section.
1. The app then parses the given file, and store the timekeeping information in
   a relational database for archival reasons.
1. After upload, the application displays a _payroll report_. The report is
   accessible to the user without them having to upload a file first.
1. If an attempt is made to upload two files with the same report id, the
   second upload should fail with an error message indicating that this is not
   allowed.

The app A sample file with the following data:

<table>
<tr>
  <th>
    date
  </th>
  <th>
    hours worked
  </th>
  <th>
    employee id
  </th>
  <th>
    job group
  </th>
</tr>
<tr>
  <td>
    4/11/2016
  </td>
  <td>
    10
  </td>
  <td>
    1
  </td>
  <td>
    A
  </td>
</tr>
<tr>
  <td>
    14/11/2016
  </td>
  <td>
    5
  </td>
  <td>
    1
  </td>
  <td>
    A
  </td>
</tr>
<tr>
  <td>
    20/11/2016
  </td>
  <td>
    3
  </td>
  <td>
    2
  </td>
  <td>
    B
  </td>
</tr>
</table>

should produce the following payroll report:

<table>
<tr>
  <th>
    Employee ID
  </th>
  <th>
    Pay Period
  </th>
  <th>
    Amount Paid
  </th>
</tr>
<tr>
  <td>
    1
  </td>
  <td>
    1/11/2016 - 15/11/2016
  </td>
  <td>
    $300.00
  </td>
</tr>
  <td>
    2
  </td>
  <td>
    16/11/2016 - 30/11/2016
  </td>
  <td>
    $90.00
  </td>
</tr>
</table>

## Application Overview

The app is composed of 3 Docker containers, `frontend`, `backend` and `db`. The frontend is built with by VueJs, the backend by Django Rest Framework, and the db is postgresql.

### Highlights

The highlights of the app include:
- Responsive frontend, styled with subtle animations
- Data is clearly presented, invites the user to sort table
- Network of Docker containers seperated by system
- Clear error messages incorperated into the interface
- Data model can be easily extended
- Admin panel for debugging data and APIs
- CSV file is never stored, only read (security)

## Setup Instructions with Docker
This has been tested using the latest Docker for OSX.

### Start The Containers

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
