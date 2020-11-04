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
> This method is not forced, you will be able to delete hosted zone, only if it doesn't have any records.


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
> This what is need to be created by you manually or provide existing one

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

## API Testsd (e2e)
> comming soon...