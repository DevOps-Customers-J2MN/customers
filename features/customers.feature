Feature: The customer service back-end
    As a Customer Service Owner
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | id | username       | password | firstname | lastname | address         | phone      | email          | active    | promo    |
        |  1 | msa503         | 503msa   | Meenakshi | Arumugam | Jersey City, NJ | 2016604601 | msa503@nyu.edu | True      | True     |
        |  2 | nuzz           | nuzzbash | Nusrath   | Basheer  | New York, NY    | 2013014018 | nuzz@nyu.edu   | False     | True     |
        |  3 | jahn           | jk56     | Jahnavi   | Kalyani  | Jersey City, NJ | 2015016019 | jk@nyu.edu     | True      | False    |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "msa503" in the results
    And I should see "nuzz" in the results
    And I should see "jahn" in the results

Scenario: Search customers based on attribute
    When I visit the "Home Page"
    And I set the "Email" to "msa503@nyu.edu"
    And I press the "Search" button
    Then I should see "msa503" in the results
    And I should not see "nuzz" in the results
    And I should not see "jahn" in the results

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "Username" to "jfy"
    And I set the "Password" to "123456"
    And I set the "Firstname" to "jinfan"
    And I set the "Lastname" to "yang"
    And I set the "Email" to "jy2296@nyu.edu"
    And I press the "Create" button
    Then I should see the message "Success"

Scenario: Retrieve a Customer
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "msa503" in the "username" field
    And I should see "Meenakshi" in the "firstname" field
    And I should see "Jersey City, NJ" in the "address" field

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "Id" to "3"
    And I press the "Retrieve" button
    Then I should see "Kalyani" in the "lastname" field
    When I change "lastname" to "Dravid"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "Id" to "3"
    And I press the "Retrieve" button
    Then I should see "Dravid" in the "lastname" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "Dravid" in the results
    Then I should not see "Kalyani" in the results

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "Id" to "100"
    And I press the "Delete" button
    Then I should see the message "Success"
    When I set the "Id" to "2"
    And I press the "Retrieve" button
    Then I should see "Nusrath" in the "firstname" field
    When I set the "Id" to "2"
    And I press the "Delete" button
    Then I should see the message "Success"
    When I set the "Id" to "2"
    And I press the "Retrieve" button
    Then I should see the message "Warning!"

Scenario: Deactive a Customer
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Deactive" button
    Then I should see the message "Success"
    And I should see "msa503" in the "username" field
    And I should see "false" in the "active" field
    And I should see "true" in the "promo" field

Scenario: Subscribe a Customer
    When I visit the "Home Page"
    And I set the "Id" to "3"
    And I press the "Promo" button
    Then I should see the message "Success"
    And I should see "jahn" in the "username" field
    And I should see "true" in the "active" field
    And I should see "true" in the "promo" field
