$(document).ready(function(){
    $('#subscriptionForm').submit(function(e){
        e.preventDefault();

        var formData = $(this).serialize();
        $.ajax({
            type: 'POST',
            url: '/',
            data: formData,
            success: function(response){
                $('#form-li').html('<p class="d-flex justify-content-start nav-link text-info">' + response.message + '</p>');
                // document.getElementById('subscriptionForm').style.display = "none";
                // $('#subscriptionMessage').text(response.message).show();
                // $('#subscriptionMessage').show();
                // $('#emailInput').val('');
            },
            error: function(response){
                $('#form-li').html('<p class="d-flex justify-content-start me-2">Произошла ошибка.</p>');
            }
        });
    });
});