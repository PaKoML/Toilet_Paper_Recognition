var submit = document.getElementById('submitButton');
submit.onclick = showImage;     //Submit 버튼 클릭시 이미지 보여주기

function showImage() {
    var newImage = document.getElementById('image-show').lastElementChild;
    newImage.style.visibility = "visible";
    
    document.getElementById('image-upload').style.visibility = 'hidden';

    document.getElementById('fileName').textContent = null;     //기존 파일 이름 지우기
}


function loadFile(input) {
    var file = input.files[0];

    var name = document.getElementById('fileName');
    name.textContent = file.name;

    var newImage = document.createElement("img");
    newImage.setAttribute("class", 'img');

    newImage.src = URL.createObjectURL(file);   

    newImage.style.width = "70%";
    newImage.style.height = "70%";
    newImage.style.visibility = "hidden";   //버튼을 누르기 전까지는 이미지 숨기기
    newImage.style.objectFit = "contain";

    var container = document.getElementById('image-show');
    container.appendChild(newImage);
};

setTimeout(function start (){
  
  $('.bar').each(function(i){  
    var $bar = $(this);
    $(this).append('<span class="count"></span>')
    setTimeout(function(){
      $bar.css('width', $bar.attr('data-percent'));      
    }, i*100);
  });

$('.count').each(function () {
    $(this).prop('Counter',0).animate({
        Counter: $(this).parent('.bar').attr('data-percent')
    }, {
        duration: 2000,
        easing: 'swing',
        step: function (now) {
            $(this).text(Math.ceil(now) +'%');
        }
    });
});

}, 500)
