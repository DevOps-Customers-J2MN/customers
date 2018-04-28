Feature: The customer service back-end
    As a Customer Service Owner
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | id | username       | password | firstname | lastname | address         | phone      | email          |
        |  1 | msa503         | 503msa   | Meenakshi | Arumugam | Jersey City, NJ | 2016604601 | msa503@nyu.edu |
        |  2 | nuzz           | nuzzbash | Nusrath   | Basheer  | New York, NY    | 201301401  | nuzz@nyu.edu   |
        |  3 | jahn           | kaly     | Jahnavi   | Kalyani  | Jersey City, NJ | 201501601  | jk@nyu.edu     | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should not see "adfg" in the results
    And I should see "msa503" in the results
    And I should see "nuzz" in the results
    And I should see "jahn" in the results
