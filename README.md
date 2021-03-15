# Website Scraper API

This is an API that allows users to scrape visible text from any website along with all static images available.
All websites are stored in postgres database and then zipped resources can be downloaded by hitting the right endpoint.
Resources can be also found in `data` folder through a connected docker volume.

# Requirements

## Basic

Installed:
* docker
* docker-compose installed
* free ports: 80, 5432
* web browser / curl

## Development

Installed:
* basic requirements
* python 3.8.6
* poetry

# Usage

## Basic

The user can:
* post a website to scrape
* check the status of a given task by returned website id
* check all websites processed with their actual statuses
* download a website resources by website id

User is prevented from posting the same website twice.
When the website fails to download the status turns to "failed" and then another attempts are allowed.


## Runtime

To start the API service run `run_app.sh` script. Please make sure that necessary ports are available.
This will startup the docker containers. If you find any issues please rebuild the docker images with `run_app_rebuild.sh` script.

## Documentation

To list endpoints and learn more about them please use the documentation included:

http://localhost:80/docs or http://localhost:80/redoc

The generated documentation allows also for usage and testing of the listed endpoints.

## Development

To start the development environment please install packages with `poetry install`
Tests for the API can be run with `run_tests.sh` script.


# Comments

To create this microservice I have decided to go with the FastAPI framework because of it's increasing popularity as the best tool to create a high performance simple API's.
The API is basic but with a full functionality. It includes validation with Pydantic models, Postgres management with SQLAlchemy and Pytest testing.


## Assumptions

* the websites don't change and once downloaded the user won't want to download it again but rather download the saved resources,
this can be easily changed if necessary to allow for posting the same website twice at different times.
User than could be prevented from posting the website twice only if the status is "pending".

* there is no persistence of postgres data through volume to avoid cleaning filesystem
* project structure is simple and suitable for microservice
* only visible text is scraped from the website, this can also be easily changed if requirements will be different
* website id is stored as an integer and doesn't need to be hidden as uuid

## Structure

* Project structure is quite simple.
For example one folder `utils` is used to store additional helpers.
This goes agains the good practice in bigger projects therefore needs to be changed if we will have to add more endpoints.
Each of the files there could be stored as a separate folder and files there.

* functions could be transformed into helper classes with each single responsibility.
This would definitely help when the project would grow bigger and would allow for extensibility.
In this case it is not necesary as simple functions are enough to manage functionality.

* The endpoints are also deliberately stored inside the main.py file for the purpose explained above.
Usually when API grows bigger we would create routes in files with the same named enpoints to keep the main file cleaner.
In this case the API is so small that it doesn't impact redeability.

## Extensions

* The API could be extended to use AWS for file storage especially if we would want to use it served on AWS instance.
Normally we would use boto3 python library to connect and transfer the zip files there.
Also some cache could be used to keep the files ~1h after creation inside the container and then only remove them.
This would save us some transfer to and from S3.

* Even though the runtime of API and tests is quite automated we could automate it more.
Example could be setting up CI/CD pipeline which would run the tests and linters automatically after each merge and then deploy the build containers to the production server.

## Problems

* The problem I ran into was containerization of the whole project.
I have decided to use the official fastapi optimized pre-build docker image and extend it with my application.
This was a little struggle because a lot of functionality there is pre-configured and therefore hidden and different from the standard Docker configuration.
Instead of using standard docker commands some are already implemented and can be changed with environment variables.
Examples would be open ports and concurrent workers.
Also the fact that the command runs automatically and we don't have to define it ourselves.
Next time I would consider manually creating the image and setting up everything explicitly.

# Summary

Overall it was a nice little project with no major blockages.
The API is clean and easily expandable if some other requirements comes along.
Also the test coverage is high and we can be sure that when changes come everything will work as it should.
