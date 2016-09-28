$( document ).ready(function() {
    $(".content-markdown").each(function () {
        var content = $(this).text();
        var markedContent = marked(content);
        console.log(markedContent);
        $(this).html(markedContent);
    });

});

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

//alert testing
$(function () {
    $('#album').click(function () {
    alert('Welcome to you album!');
    });
})
