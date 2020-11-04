import boto3
from src.environment import Environment


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
        pass