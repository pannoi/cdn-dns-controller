Feature: List Hosted Zones
 In order to list hosted zones
 As a developer
 I want to send GET request
 So that API will return all hosted zones from Route53

Background:
   Given I set api url to list zones "http://localhost:5000"

Scenario: GET posts to list hosted zones
 Given I set GET posts api endpoint to list zones "/zones"
  When I set HEADER param request content to list zones type as "application/json"
  Then I receive valid HTTP response code "200" for "GET" to list zones
	And Response BODY "GET" is non-empty to list zones
