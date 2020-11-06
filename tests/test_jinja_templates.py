import jinja2
import pytest


def prerender(filename, context):
    path = 'templates'
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(filename).render(context)


@pytest.mark.parametrize('comment, action, name, type, ttl, target', [
    ('some_comment', 'UPSERT', 'super_name', 'A', '300', '8.8.8.8'),
    ('cool_comment', 'UPSERT', 'ultra_name', 'CNAME', '60', 'google.com')
])
def test_record_set_template(comment, action, name, type, ttl, target):
    filename = 'resource_record_set.j2'

    context = {
        'comment': comment,
        'action': action,
        'name': name,
        'type': type,
        'ttl': ttl,
        'target': target
    }
    rendered = prerender(filename, context)

    for val in context.values():
        assert val in rendered


@pytest.mark.parametrize('comment, action, evaluate_health, dns_name, hosted_zone, name, type',[
    ('test_alias', 'UPSERT', 'False', 'example.com', 'ID123', 'example.com', 'A'),
])
def test_record_alias_template(comment, action, evaluate_health, dns_name, hosted_zone, name, type):
    filename = 'resource_record_alias.j2'
    context = {
        'comment': comment,
        'action': action,
        'evaluate_health': evaluate_health,
        'dns_name': dns_name,
        'hosted_zone': hosted_zone,
        'name': name,
        'type': type
    }
    rendered = prerender(filename, context)

    for val in context.values():
        assert val in rendered

    
@pytest.mark.parametrize('cal_ref, comment, origin_id, domain_name, endpoint, certificate', [
    ('123321', 'comment', 'example.com', 'example.com', 'google.com', 'arn://test.amazonaws.com')
])
def test_cdn_default_template(cal_ref, comment, origin_id, domain_name, endpoint, certificate):
    filename = 'cdn_distribution_default.j2'
    context = {
        'caller_reference': cal_ref,
        'comment': comment,
        'origin_id': origin_id,
        'domain_name': domain_name,
        'endpoint': endpoint,
        'certificate': certificate
    }
    rendered = prerender(filename, context)

    for val in context.values():
        assert val in rendered
