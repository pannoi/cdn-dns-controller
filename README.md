# cdn-dns-controller

[![Build Status](https://travis-ci.org/pannoi/cdn-dns-controller.svg?branch=main)](https://travis-ci.org/pannoi/cdn-dns-controller)

[![codecov](https://codecov.io/gh/pannoi/cdn-dns-controller/branch/main/graph/badge.svg?token=11VG1ME7GE)](https://codecov.io/gh/pannoi/cdn-dns-controller)


Is a controller which implements API model to manage Route53 records and CDN controllers.

Could be usefull if you are having your own AWS ecosystem and CMS platform/hosting to automate CDN and DNS record management

- [cdn-dns-controller](#cdn-dns-controller)
    - [TODO](#todo)
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


## TODO

- Cover whole api methods with e2e BDD tests
- Add logging module to handle exceptions and print out information
- Automatically get CDN hosted zone ID and remove it from env. variables
- Add additinional templates for CDN creation to optimize caching behavior

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
            "Private": true | false
        }
    ```
- [X] `POST` /zones/<zone_id> -> creates/updates/deletes record set/alias under specific hosted zone
    - __Example (Set):__
        ```json
            {
                "RecordType": "Set",
                "Comment": "some example comment",
                "Action": "CREATE | DELETE | UPSERT",
                "Name": "example.com", // Your record name
                "Type": "'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'",
                "TTL": "<int>", // Whatever integer to determine TTl
                "Target": "<string>" // Whatever endpoint to map your record (list)
            }
        ```
    - __Example (Alias):__
        ```json
            {
                "RecordType": "Alias",
                "Comment": "some example comment",
                "Action": "CREATE | DELETE | UPSERT",
                "Type": "'SOA'|'A'|'TXT'|'NS'|'CNAME'|'MX'|'NAPTR'|'PTR'|'SRV'|'SPF'|'",
                "HostedZone": "<string>", // Hosted Zone of resource where resource is located
                "DnsName": "<string>", // Target Address
                "Name": "<string>" // example.example.com (name.domain.name)
            }
        ```
    > Record sets/aliases deletion methods covers in POST request (just provide DELETE action)
- [X] `DELETE` /zones/<zone_id> -> delete route53 hosted zone
> IF you'd like to have force deletiong please add force=true parameter

```js
    /zones/<zone_id>?force=true
```


## Clodfront module

- [X] `GET` /distributions/ -> lists all CDN distributions in Cloudfront domain
- [X] `GET` /distributions/<distribution_id> -> lists all information about specific distribution
- [X] `POST` /distributions/ -> create new CDN distribution
    - __Example:__
        ```json
            {
                "Comment": "<string>", // Comment for CDN
                "OriginId": "<string>", // Origin which should be assigned for CDN
                "DomainName": "<string>", // Domain name what should be assigned for CDN
                "HostedZone": "<string>", // HostedZone where record shouldbe created (ID)
                "Endpoint": "<string>" // For example: ELB
            }
        ```
- [X] `DELETE` /distributions/<distribution_id> -> delete specified distribution from Cloudfront

# Run

## .env
* __AWS_ACCESS_KEY__ = AWS ACCESS KEY FOR IAM 
* __AWS_SECRET_KEY__ = AWS SECRET KEY FOR IAM
* __AWS_REGION__ = region where iam will be connected to AWS
> Tested Region us-east-1
* __ROUTE53_DELEGATION_SET__ = route53 delegation set which will be used for creating hosted zones 
> This what is need to be created by you manually or provide existing one
* __CDN_HOSTED_ZONE_ID__ = hosted zone id for cdn

## Local

```bash
python -u main.py
```

## Docker 

```bash
docker run -it -d -p 5000:5000 -e AWS_ACCESS_KEY="" -e AWS_SECRET_KEY="" -e AWS_REGION="" -e "" --rm --name cdn-dns-controller ${image_name}:${image_tag}
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

## API tests
> To run this tests controller should be up and running with ENV variables to be able to connect to AWS

* __Source:__ e2e/

* __HowToRun:__

	```bash
	python3 -m behave e2e/
	```

* __Schema:__

	- __*.feature__ - Here is describe API feature from user point of view
	- __steps/__ 	- Here is describe real tests using python to implement features
