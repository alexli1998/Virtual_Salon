var img = ''

function upload_img() {
    var formData = new FormData();
        formData.append('file', $("#upload_img")[0].files[0]);
//        alert(formData.get('file').name)
        $.ajax({
                url: '/upload_img',
                type: 'post',
                data: formData,
                processData: false,
                contentType: false,
                dataType: 'text',
                success: function () {
                    img = formData.get('file').name
                    $.getJSON('/upload_img', {'img': img}, function(response) {
                        document.getElementById('userimg').src = response.url
                    });
                },
                error: function(response) {

                }
        });

}

$(function() {
    $("#generate").click(function (event) {
        $.ajax({
                url: '/generate',
                type: 'post',
                data: {'img': img},
                dataType: 'json',
                success: function() {
                    $.getJSON('/generate', {'img': img}, function(response) {
                        document.getElementById('recimg').src = response.url
                    });
                },
                error: function(response) {

                }
        });
    });
});

$(".hairstyle").click(function(){
    $(this).addClass("sel");
    $(this).siblings('.hairstyle').removeClass("sel");
});

$(".color").click(function(){
    $(this).addClass("sel");
    $(this).siblings('.color').removeClass("sel");
});