import boto3
from jinja2 import Environment as jEnv
from jinja2 import Template, FileSystemLoader
import time

from src.environment import Environment
from src.acm import ACM
from src.helpers import Helper
from src.route53 import Route53


class CloudFront():
    """ Class describes CloudFront interface. """
    def __init__(self):
        """ Class constructor. """
        self.client = boto3.client(
            'cloudfront',
            aws_access_key_id = Environment.aws_access_key,
            aws_secret_access_key = Environment.aws_secret_key,
            region_name = Environment.aws_region
        )


    def list_distirbutions(self):
        """ Lists infromation about all CDN distribution. """
        return self.client.list_distirbutions()


    def get_distribution(self, distribution_id):
        """
        Lists inforamtion about specific distribution by id.

        :param distribution_id: Id of CDN distribution
        """
        return self.client.get_distribution(
            Id=distribution_id
        )


    def delete_distribution(self, distribution_id):
        """
        Deletes CDN distribution

        :param distribution_id: Id of CDN distribution
        """
        acm = ACM()
        result = self.client.delete_distribution(
            Id=distribution_id
        )
        certificate_arn = result['DistributionConfig']['ViewerCertificate']['ACMCertificateArn']
        self.wait_for_distribution_deletion(distribution_id=distribution_id)
        acm.delete_certificate(certificate_arn=certificate_arn)
        return result

    
    def wait_for_distribution_deletion(self, distribution_id, sleep_time=5, timeout=600):
        """
        Function waits until distribution will be disabled to delete it and remove certificate.

        :param distribution_id : Id of CDN distribution
        :param sleep_time      : default 5 sec, checks certificate status every 5 seconds
        :param timeout         : maximum time to try certificate verification
        """
        status = self.get_distribution(distribution_id)['DistributionConfig']['Status']
        elapsed_time = 0
        while status == 'InProgress':
            if elapsed_time > timeout:
                raise Exception('Timeout ({}s) reached for CDN distribution deletion'.format(timeout))
            time.sleep(sleep_time)
            status = self.get_distribution(distribution_id)['DistributionConfig']['Status']
            elapsed_time += sleep_time


    def create_distribution(self, comment, origin_id, domain_name, hosted_zone, endpoint):
        """
        Function creates new CDN distribution.

        :param comment     : Comment to new distribution
        :param origin_id   : Origin_id of new distribution
        :param domain_name : Domain Name which will be assigned to new distribution
        :param hosted_zone : Hosted zone where should be record for cdn created
        :param endpoint    : Endpoint what should be mapped for CDN, ussualy ELB
        """
        acm = ACM()
        helpers = Helper()
        certificate = acm.request_certificate(domain_name=domain_name)
        time.sleep(5)
        record = acm.get_domain_validation_records(certificate_arn=certificate)
        acm.create_dns_record(record=record, zone_id=hosted_zone)
        acm.wait_for_certificate_validation(certificate_arn=certificate)
        caller_reference = helpers.get_random_string(13)
        file_loader = FileSystemLoader('templates')
        env = jEnv(loader=file_loader)
        env.trim_blocks = True
        template = env.get_template('cdn_distribution_default.j2')
        output = template.render(
            caller_reference=caller_reference,
            comment=comment.arg,
            origin_id=origin_id,
            domain_name=domain_name,
            endpoint=endpoint,
            certificate=certificate
        )
        new_cdn = self.client.create_distribution(
            DistributionConfig=output
        )
        # Create record to route trafic via CDN
        route53 = Route53()
        route53.change_resource_record_alias(
            zone_id=hosted_zone,
            comment=comment,
            action="UPSERT",
            type='A',
            hosted_zone=Environment.cdn_hosted_zone,
            dns_name=new_cdn['Distribution']['DomainName'],
            name=domain_name
        )
        return new_cdn
