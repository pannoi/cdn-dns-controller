Feature: List CDN Distributions
 In order to list cdn distributions
 As a developer
 I want to send GET request
 So that API will return all distributions from CloudFront

Background:
   Given I set api url to list distributions "http://localhost:5000"

Scenario: GET posts to list distributions
 Given I set GET posts api endpoint to list distributions "/distributions"
  When I set HEADER param request content to list distributions type as "application/json"
  Then I receive valid HTTP response code "200" for "GET" to list distributions
	And Response BODY "GET" is non-empty to list distributions
