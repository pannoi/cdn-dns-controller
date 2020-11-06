import boto3
from jinja2 import Environment as jEnv
from jinja2 import Template, FileSystemLoader
import time

from src.environment import Environment
from src.acm import ACM


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


    def create_distribution(self):
        """
        Function creates new CDN distribution.
        
        :param 
        """
        pass


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
