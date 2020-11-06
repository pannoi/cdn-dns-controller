import boto3
import time
from src.environment import Environment


class ACM():
    """ Class to interact with AWS ACM to manage certificates. """
    def __init__(self):
        """ Class constructor. """
        self.client = boto3.client(
            'acm',
            aws_access_key_id = Environment.aws_access_key,
            aws_secret_access_key = Environment.aws_secret_key,
            region_name = Environment.aws_region
        )


    def list_certificates(self):
        """ Lists all certificates in ACM. """
        return self.client.list_certificates(
            MaxItems = 123
        )


    def get_certificate(self, certificate_arn):
        """
        Lists certificate information by certificate ARN.

        :param certificate_arn: unique certificate_arn provided by amazon
        """
        return self.client.get_certificate(
            CertificateArn = certificate_arn
        )


    def request_certificate(self, domain_name):
        """
        Requests certificate from ACM.

        :param domain_name: domain name for certificate signing
        """
        response = self.client.request_certificate(
            DomainName=domain_name,
            ValidationMethod='DNS',
        )
        return response.get('CertificateArn')


    def delete_certificate(self, certificate_arn):
        """
        Deletes certificate from ACM by certificate ARN.

        :param certificate_arn: unique certificate_arn provided by amazon
        """
        return self.client.delete_certificate(
            CertificateArn=certificate_arn
        )


    def get_domain_validation_records(self, certificate_arn):
        """
        When certificate is created it needs to be verified by domain record.
        Method returns this validation record which needs to be set in Route53.

        :param certificate_arn: unique certificate_arn provided by amazon
        """
        certificate_metadata = self.client.describe_certificate(
            CertificateArn=certificate_arn
        )
        return certificate_metadata.get('Certificate', {}).get('DomainValidationOptions', [])


    def get_resource_record_data(self, r):
        """
        Parsing function for record_set dict.

        :param r: record_set dictionary from method -> get_domain_validation_records()	
        """
        return (r.get('Type'), r.get('Name'), r.get('Value'))


    def wait_for_certificate_validation(self, certificate_arn, sleep_time=5, timeout=300):
        """
        Method to wait until certificate will be valid with timeout.

        :param certificate_arn : unique certificate_arn provided by amazon
        :param sleep_time      : default 5 sec, checks certificate status every 5 seconds
        :param timeout         : maximum time to try certificate verification
        """
        status = self.client.describe_certificate(CertificateArn=certificate_arn)['Certificate']['Status']
        elapsed_time = 0
        while status == 'PENDING_VALIDATION':
            if elapsed_time > timeout:
                raise Exception('Timeout ({}s) reached for certificate validation'.format(timeout))
            time.sleep(sleep_time)
            status = self.client.describe_certificate(CertificateArn=certificate_arn)['Certificate']['Status']
            elapsed_time += 5
