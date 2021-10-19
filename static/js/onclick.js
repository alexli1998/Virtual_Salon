var img = ''
var ref = ''
var color = ''

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

$("#recommend").click(function () {
  $("#generate").css('display', 'inline')
});

$("#generate").click(function (event) {
    $.ajax({
            url: '/generate',
            type: 'post',
            data: {'img': img, 'color': color, 'ref': ref},
            dataType: 'json',
            beforeSend :function(xmlHttp){
              xmlHttp.setRequestHeader("If-Modified-Since","0");
              xmlHttp.setRequestHeader("Cache-Control","no-cache");
             },
            success: function() {
                $.getJSON('/generate', {'img': img, 'color': color, 'ref': ref}, function(response) {
                  document.getElementById('genimg').src = response.url + '?' + Math.random()
                  $("#adjust").css('display', 'inline')
                });
            },
            error: function(response) {

            }
    });
});

$(".hairstyle").click(function(){
  $(this).addClass("sel");
  $(this).siblings('.hairstyle').removeClass("sel");
  ref = $(this).attr('src')
  console.log(ref)
});

$(".color").click(function(){
  $(this).addClass("sel");
  $(this).siblings('.color').removeClass("sel");
  color = $(this).attr('id')
  console.log(color)
});