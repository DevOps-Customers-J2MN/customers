# customers

[![Build Status](https://travis-ci.org/DevOps-Customers-J2MN/customers.svg?branch=master)](https://travis-ci.org/DevOps-Customers-J2MN/customers)
[![codecov](https://codecov.io/gh/DevOps-Customers-J2MN/customers/branch/master/graph/badge.svg)](https://codecov.io/gh/DevOps-Customers-J2MN/customers)

Production URL : https://nyu-customer-service-s18.mybluemix.net/

This is the repository for squads "/customers"

The base service code is contained in `server.py` while the business logic for manipulating Customers is in the `models.py` file. As such, we have two tests suites: one for the model (`test_customers.py`) and one for the serveice itself (`test_server.py`)

## Prerequisite Installation

The easiest way to use this repo is with Vagrant and VirtualBox. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant:

    git clone https://github.com/DevOps-Customers-J2MN/customers
    cd customers
    vagrant up
    vagrant ssh
    cd /vagrant

You can now start the server by

    $ python run.py

When you are done, you can exit and shut down the vm with:

    $ exit
    $ vagrant halt

If the VM is no longer needed you can remove it with:

    $ vagrant destroy

## Running the Tests

#### Run the unit tests using `nose`

    $ nosetests

Nose is configured to automatically run the `coverage` tool and you should see a percentage of coverage report at the end of your tests. If you want to see what lines of code were not tested use:

    $ coverage report -m

You can also run the Code Coverage tool manually without `nosetests` to see how well test cases exercise code:

    $ coverage run test_server.py
    $ coverage report -m --include=server.py

You can also manually run `nosetests` with `coverage` (but `setup.cfg` does this already)

    $ nosetests --with-coverage --cover-package=server

#### Run the Behavioral Driven Development tests using `Behave` and `Selenium`

First, you need to run the server in the background

    $ python run.py &

Then you can run the BDD tests
    
    $ behave
    
After the BDD tests, we need to bring the server to the foreground to stop it since we started the server in the background with '&'

    $ fg
    $ <ctrl + c>

## What's featured in the project?

    * app/server.py -- the main Service using Python Flask
    * app/models.py -- the data model using Redis
    * tests/test_server.py -- test cases against the service
    * tests/test_customers.py -- test cases against the Customer model
