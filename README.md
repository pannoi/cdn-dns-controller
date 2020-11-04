# cdn-dns-controller

- [cdn-dns-controller](#cdn-dns-controller)
- [General](#general)
- [Methods](#methods)
    - [Route53 module](#route53-module)
    - [Cloudfront module](#cloudfront-module)
- [Run](#run)
    - [.env](#.env)
    - [Local](#local)
    - [Docker](#docker)
- [Tests](#tests)
    - [Unit tests](#unit-tests)
    - [API tests](#api-tests)

# General

# Methods

## Route53 module

- [X] `GET` /zones/ -> lists all hosted zones in Route53 domain
- [X] `GET` /zones/<zone_id> -> lists all record sets in specific hosted zone
- [X] `POST` /zones/ -> create new hosted_zone
    __Example:__
    ```json
        {
            "Name": "example.com",
            // Optional
            "Comment": "some example comment",
            "Private": true || false
        }
    ```
- [ ] `POST` /zones/<zone_id> -> create new record set under specific hosted zone
- [ ] `DELETE` /zones/<zone_id> -> delete route53 hosted zone
- [ ] `DELETE` /zones/<zone_id>/<record_name> -> delete record set under hosted zone

## Clodfront module

- [X] `GET` /distributions/ -> lists all CDN distributions in Cloudfront domain
- [X] `GET` /distributions/<distribution_id> -> lists all information about specific distribution
- [ ] `POST` /distributions/ -> create new CDN distribution
- [ ] `DELETE` /distributions/<distribution_id> -> delete specified distribution from Cloudfront

# Run

## .env
* __AWS_ACCESS_KEY__ = AWS ACCESS KEY FOR IAM 
* __AWS_SECRET_KEY__ = AWS SECRET KEY FOR IAM
* __AWS_REGION__ = region where iam will be connected to AWS
> Tested Region us-east-1
* __ROUTE53_DELEGATION_SET__ = route53 delegation set which will be used for creating hosted zones 

## Local

```bash
python -u main.py
```

## Docker 

```bash
docker run -it -d -p 5000:5000 -e AWS_ACCESS_KEY="" -e AWS_SECRET_KEY="" -e AWS_REGION="" --rm --name cdn-dns-controller ${image_name}:${image_tag}
```
> image_name = repository name of docker image
> image_tag = specify version what do you like to upload

# Tests

## Unit tests

> Runs static unit tests to verify functionality

* __Source:__ tests/

* __HowToRun:__
    - ```bash
        python -m pytest tests/
      ```
* __Schema:__
	- __context.py__ - Context to import modules from src directory
	- __test_*.py__  - Unit tests

## API Testsd (e2e)
> comming soon...