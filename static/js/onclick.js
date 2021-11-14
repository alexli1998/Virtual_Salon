var img = ''
var ref = ''
var color = ''
var encimg

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
  $.ajax({
    url: '/recommendation',
    type: 'post',
    data: {'img': img},
    dataType: 'json',
    success: function (response) {
      document.getElementById('rec1').src = response.url1
      document.getElementById('rec2').src = response.url2
      document.getElementById('rec3').src = response.url3
    },
    error: function(response) {

    }
  });
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

$(".hairstyle").click(function () {
  if ($(this).attr('class') == 'hairstyle sel') {
    $(this).removeClass("sel");
    hairstyle = ""
  } else {
    $(this).addClass("sel");
    $(this).siblings('.hairstyle').removeClass("sel");
    ref = $(this).attr('src')
    console.log(ref)
  }
});

$(".color").click(function () {
  if ($(this).attr('class') == 'color sel') {
    $(this).removeClass("sel");
    color = ""
  } else {
    $(this).addClass("sel");
    $(this).siblings('.color').removeClass("sel");
    color = $(this).attr('id')
    console.log(color)
  }
});

$("#adjust").click(function () {
  $.ajax({
    url: '/adjust',
    type: 'post',
    data: {'img': img},
    dataType: 'json',
    success: function (response) {
      encimg = response
      $("#adjustbar").css('display', 'inline')    
    },
    error: function() {}
  });
});

$("#adjustbar").change(function() {
  document.getElementById('adjimg').src = encimg[document.getElementById("adjustbar").value]
});