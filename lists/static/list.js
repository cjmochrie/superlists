/**
 * Created by Cameron on 11/3/2015.
 */
jQuery(document).ready(function() {

     $('#id_text').on('click', function () {
        $('.has-error').hide();
    });

    $('#id_text').on('keypress', function () {
        $('.has-error').hide();
    });

});