Feature: The customer service back-end
    As a Customer Service Owner
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | id | username       | password | firstname | lastname | address         | phone      | email          | status | promo |
        |  1 | msa503         | 503msa   | Meenakshi | Arumugam | Jersey City, NJ | 2016604601 | msa503@nyu.edu | 1      | 1     |
        |  2 | nuzz           | nuzzbash | Nusrath   | Basheer  | New York, NY    | 201301401  | nuzz@nyu.edu   | 0      | 0     |
        |  3 | jahn           | kaly     | Jahnavi   | Kalyani  | Jersey City, NJ | 201501601  | jk@nyu.edu     | 1      | 0     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "msa503" in the results
    And I should see "nuzz" in the results
    And I should see "jahn" in the results

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "Username" to "jfy"
    And I set the "Password" to "123456"
    And I set the "Firstname" to "jinfan"
    And I set the "Lastname" to "yang"
    And I set the "Email" to "jy2296@nyu.edu"
    And I press the "Create" button
    Then I should see the message "Success"
