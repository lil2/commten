$( document ).ready(function() {
    post_ajax_signup_form();
    $(".content-markdown").each(function () {
        var content = $(this).text();
        console.log(content);
        var markedContent = marked(content);
        console.log(markedContent);
        $(this).html(markedContent);
    });

});



// Passing user signup values in modal to backend using ajax
function post_ajax_signup_form() {
    $( document ).on('submit','#new_user_form', function (e) {
       e.preventDefault();
        $.ajax({
            type:'POST',
            url: '/user/create/',
            data:{
                name: $('#new_user_username').val(),
                pwd: $('#new_user_password').val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success:function () {
                alert("Welcome New User!");
                window.location = "/";
            }
        });
    });
}


// Sending ajax to toggle button on following
function follow_btn(caller) {
    $.ajax({
        type:'POST',
        url: '/follows/',
        data:{
            follow_id: caller.attr('id'),
            follow_text : caller.text(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success:function (json) {
           caller.text(json['status']);
            if (json['status'] == 'Follow'){
                caller.removeClass('btn-primary');
                caller.addClass('btn-warning');
            }
            else{
                caller.removeClass('btn-warning');
                caller.addClass('btn-primary');
            }
        }
    });
}