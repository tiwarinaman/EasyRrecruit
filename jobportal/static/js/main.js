// Preloader

function load() {
    document.getElementById("overlayer").style.display = 'none';
}


// To make Active Navbar

$(document).ready(function () {
    $('#btn-loader').hide();
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


