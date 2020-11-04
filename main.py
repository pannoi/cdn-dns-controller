from flask import Flask, jsonify
from flask import make_response
from flask import request

from src.route53 import Route53
from src.cloudfront import CloudFront

app = Flask(__name__)


# Route53 routes
@app.route('/zones/', methods=['GET'])
def list_hosted_zones():
    """ Function lists all hosted zones in Route53. """
    route53 = Route53()
    return route53.list_hosted_zones()


@app.route('/zones/<string:zone_id>', methods=['GET'])
def get_hosted_zone(zone_id):
    """
    Function return the hosted zone information

    :param zone_id: Id of hosted zone to GET record sets.
    """
    route53 = Route53()
    return route53.get_hosted_zone(zone_id=zone_id)


@app.route('/zones/', methods=['POST'])
def create_hosted_zone():
    """ Function creates new hosted zone under Route53 domain. """
    route53 = Route53()
    data = request.get_json()
    hz_name = data['Name']
    comment = data['Comment'] if data['Comment'] else ""
    is_private = data['Private'] if data['Private'] else False
    return route53.create_hosted_zone(domain_name=hz_name, comment=comment, is_private=is_private)


# CloudFront routes
@app.route('/distributions/', methods=['GET'])
def list_distributions():
    """ Lists infromation about all CDN distribution. """
    cloudfront = CloudFront()
    return cloudfront.list_distirbutions()


@app.route('/distributions/<string:distribution_id>', methods=['GET'])
def get_distributions(distribution_id):
    """
    Lists inforamtion about specific distribution by id.

    :param distribution_id: Id of CDN distribution
    """
    cloudfront = CloudFront()
    return cloudfront.get_distribution(distribution_id=distribution_id)


@app.errorhandler(404)
def not_found():
    """ If route is not defined on backend -> return 404. """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
