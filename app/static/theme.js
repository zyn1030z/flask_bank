$(document).ready(function () {
    $('.nav-item .nav-link').click(function () {
        $('.nav-item .nav-link').removeClass('active');
        $(this).addClass('active');
    })
});