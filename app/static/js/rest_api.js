$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#inputID").val(res.id);
        $("#inputUsername").val(res.username);
        $("#inputPassword").val(res.password);
        $("#inputEmail").val(res.email);
        $("#inputFirstname").val(res.firstname);
        $("#inputLastname").val(res.lastname);
        $("#inputPhone").val(res.phone);
        $("#inputAddress").val(res.address);
        if (res.active == true) {
            $("#inputActive").val("true");
        } else {
            $("#inputActive").val("false");
        }
        if (res.promo == true) {
            $("#inputPromo").val("true");
        } else {
            $("#inputPromo").val("false");
        }
    }

    // Clears all form fields
    function clear_form_data() {
        $("#inputID").val("");
        $("#inputUsername").val("");
        $("#inputPassword").val("");
        $("#inputEmail").val("");
        $("#inputFirstname").val("");
        $("#inputLastname").val("");
        $("#inputPhone").val("");
        $("#inputAddress").val("");
        $("#inputActive").val("");
        $("#inputPromo").val("");
    }

    // ****************************************
    // Retrieve a Customers
    // ****************************************
    $("#retrieve-btn").click(function () {
        var customer_id = $("#inputID").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/customers/" + customer_id,
            contentType:"application/json",
            data: ''
        });

        ajax.done(function(res){
            update_form_data(res)
            window.alert("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            window.alert("Failed")
        });
    });


    // ****************************************
    // Delete a Customer
    // ****************************************
    $("#delete-btn").click(function () {
       var customer_id = $("#inputID").val();

       var ajax = $.ajax({
           type: "DELETE",
           url: "/customers/" + customer_id,
           contentType:"application/json",
           data: '',
       })

       ajax.done(function(res){
           clear_form_data()
           window.alert("Success")
       });

       ajax.fail(function(res){
           window.alert("Delete failed!")
       });
     });


     // ****************************************
     // Search for a Customer
     // ****************************************
     $("#search-btn").click(function () {
        var username = $("#inputUsername").val();
        var email = $("#inputEmail").val();
        var firstname = $("#inputFirstname").val();
        var lastname = $("#inputLastname").val();
        var phone = $("#inputPhone").val();
        var address = $("#inputAddress").val();
        var active = $("#inputActive").val() == "true";
        var promo = $("#inputPromo").val() == "true";

        var queryString = ""
        if (username) {
            queryString += 'username=' + username
        }
        if (email) {
            if (queryString.length > 0) {
                queryString += '&email=' + email
            } else {
                queryString += 'email=' + email
            }
        }
        if (firstname) {
            if (queryString.length > 0) {
                queryString += '&firstname=' + firstname
            } else {
                queryString += 'firstname=' + firstname
            }
        }
        if (lastname) {
            if (queryString.length > 0) {
                queryString += '&lastname=' + lastname
            } else {
                queryString += 'lastname=' + lastname
            }
        }
        if (phone) {
            if (queryString.length > 0) {
                queryString += '&phone=' + phone
            } else {
                queryString += 'phone=' + phone
            }
        }
        if (address) {
            if (queryString.length > 0) {
                queryString += '&address=' + address
            } else {
                queryString += 'address=' + address
            }
        }
        if (active) {
            if (queryString.length > 0) {
                queryString += '&active=' + active
            } else {
                queryString += 'active=' + active
            }
        }
        if (promo) {
            if (queryString.length > 0) {
                queryString += '&promo=' + promo
            } else {
                queryString += 'promo=' + promo
            }
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/customers?" + queryString,
            contentType:"application/json",
            data: ''
        })

        ajax.done(function(res){
            window.alert("Success");
            $("#search_results").empty();
            var table = '<table class="table table-hover">';
            var header = '<thead><tr>';
            header += '<th scope="col">ID</th>';
            header += '<th scope="col">UserName</th>';
            header += '<th scope="col">Email</th>';
            header += '<th scope="col">FirstName</th>';
            header += '<th scope="col">LastName</th>';
            header += '<th scope="col">PhoneNumber</th>';
            header += '<th scope="col">Address</th>';
            header += '<th scope="col">Active</th>';
            header += '<th scope="col">Promo</th>';
            header += '</tr></thead>';
            table += header;
            var body = '<tbody>';
            for(var i = 0; i < res.length; i++) {
                customer = res[i];
                var row = '<tr>';
                row += '<td>' + customer.id + '</td>';
                row += '<td>' + customer.username + '</td>';
                row += '<td>' + customer.email + '</td>';
                row += '<td>' + customer.firstname + '</td>';
                row += '<td>' + customer.lastname + '</td>';
                row += '<td>' + customer.phone + '</td>';
                row += '<td>' + customer.address + '</td>';
                row += '<td>' + customer.active + '</td>';
                row += '<td>' + customer.promo + '</td>';
                row += '</tr>';
                body += row;
            }
            body += '</tbody>';
            table += body;
            table += '</table>';
            $("#search_results").append(table);
        });

        ajax.fail(function(res){
            window.alert("Search failed!");
        });
    });


    // ****************************************
    // Clear the form
    // ****************************************
    $("#clear-btn").click(function () {
        clear_form_data()
    });


    // ****************************************
    // Create a Customer
    // ****************************************
    $("#create-btn").click(function () {
        var username = $("#inputUsername").val();
        var password = $("#inputPassword").val();
        var email = $("#inputEmail").val();
        var firstname = $("#inputFirstname").val();
        var lastname = $("#inputLastname").val();
        var phone = $("#inputPhone").val();
        var address = $("#inputAddress").val();
        var active = $("#inputActive").val() == "true";
        var promo = $("#inputPromo").val() == "true";

        var data = {
            "username": username,
            "password": password,
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "phone": phone,
            "address": address,
            "active": active,
            "promo": promo
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/customers",
            contentType:"application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            window.alert("Sucess!")
        });

        ajax.fail(function(res){
            window.alert("Failed!")
        });
    });

    // ****************************************
    // Update a Customer
    // ****************************************
    $("#update-btn").click(function () {
        var customer_id = $("#inputID").val();
        var username = $("#inputUsername").val();
        var password = $("#inputPassword").val();
        var email = $("#inputEmail").val();
        var firstname = $("#inputFirstname").val();
        var lastname = $("#inputLastname").val();
        var phone = $("#inputPhone").val();
        var address = $("#inputAddress").val();
        var active = $("#inputActive").val() == "true";
        var promo = $("#inputPromo").val() == "true";

        var data = {
            "username": username,
            "password": password,
            "email": email,
            "firstname": firstname,
            "lastname": lastname,
            "phone": phone,
            "address": address,
            "active": active,
            "promo": promo
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/customers/" + customer_id,
                contentType:"application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            window.alert("Success")
        });

        ajax.fail(function(res){
            window.alert("Failed")
        });

    });
})
