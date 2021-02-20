// Load after document is ready

$(document).ready(function () {

    // Hide Preloader
    $("#overlayer").hide();

    // Hide the button after loading the data
    $('#btn-loader').hide();

    // Make Navbar Active
    let url = window.location;
    $('ul.navbar-nav a[href="' + url + '"]').parent().addClass('active-nav');
    $('ul.navbar-nav a').filter(function () {
        return this.href == url;
    }).parent().addClass('active-nav').siblings().removeClass('active-nav');
});

// Button Loader for apply job
$("form").submit(function () {
    $('#submit').hide();
    $('#btn-loader').show();
    $('#btn-loader').attr('disabled', 'disabled');
});


