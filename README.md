# CourierIIIT

A complete overhaul of the IIITH Couriers Portal with additional features such as e-mail notifications and package protection.

## Overview

CourierIIIT will maintain a list of your packages still with security, along with some metadata related to those packages. It will send an automated email notification upon receiving a new package, and maintains a log of all your packages ever received by Nilgiri security.

It has a login for security personnel as well, where they have the option to either add another package, or release a package currently kept with them.

There is also a separate login portal for admins to add student and security IDs.

## Usage

Navigate to the repository in the terminal and run using:

``` flask run ```

Admin credentials are username: aks, password: aks123

## Configuration

The program requires two environment variables to be set, namely MY_EMAIL and MY_PASSWORD which are valid credentials to an email account (preferably outlook) through which to send otp and password emails to the users.

## Folder Structure

- ``` ./templates ``` - Stores all the HTML pages required for the site
- ```./app.py ``` - Contains most of the backend, including the functions to get and post to the database, control routes, navigate through the website, etc.
- ``` ./helper.py ``` - Contains some helper functions
- ``` iiit-courier.db ``` - SQLite3 database which stores info in 4 tables: admins, couriers, students and security
  - admins stores admin IDs and passwords
  - packages stores courier ID, security ID, student roll number, arrival and collection time, collection status and source
  - students stores names, roll numbers and email IDs
  - security stores security IDs, names and email IDs

## Contributing

Aks Kanodia <br>
Raghav Doshi <br>
Ronit Jalihal <br>
Yajat Rangekar <br>

## Credits

### Python packages:
- werkzeug.security
- secrets
- SQL from cs50
- flask

_An honorary mention to ChatGPT :)_

## Thank you!
