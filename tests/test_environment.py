import os


def test_aws_access_key():
    aws_access_key = os.getenv('AWS_ACCESS_KEY', default=None)
    if aws_access_key is None:
        raise OSError("AWS_ACCESS_KEY is not set")


def test_aws_secret_key():
    aws_secret_key = os.getenv('AWS_SECRET_KEY', default=None)
    if aws_secret_key is None:
        raise OSError("AWS_SECRET_KEY is not set")


def test_aws_region():
    aws_region = os.getenv('AWS_REGION', default=None)
    if aws_region is None:
        raise OSError("AWS_REGION is not set")


def test_route53_delegation_set():
    route53_delegation_set = os.getenv('ROUTE53_DELEGATION_SET', default=None)
    if route53_delegation_set is None:
        raise OSError("ROUTE53_DELEGATION_SET is not set")


def test_cdn_hosted_zone():
    cdn_hosted_zone = os.getenv('CDN_HOSTED_ZONE_ID', default=None)
    if cdn_hosted_zone is None:
        raise OSError("CDN_HOSTED_ZONE_ID is not set")
