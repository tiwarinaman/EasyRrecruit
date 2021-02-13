
function load() {
    document.getElementById("overlayer").style.display = 'none';
}


// To make Active Navbar Code

$(document).ready(function () {
    var url = window.location;
    $('ul.navbar-nav a[href="' + url + '"]').parent().addClass('active-nav');
    $('ul.navbar-nav a').filter(function () {
        return this.href == url;
    }).parent().addClass('active-nav').siblings().removeClass('active-nav');
});
