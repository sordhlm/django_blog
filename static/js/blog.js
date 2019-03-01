$(document).ready(function() {
    // 获取弹窗
    var modal = document.getElementById('myModal');
     
    // 打开弹窗的按钮对象
    var btn = document.getElementById("myBtn");
     
    // 获取 <span> 元素，用于关闭弹窗
    var span = document.querySelector('.close');
     
    // 点击按钮打开弹窗
   //btn.onclick = function() {
   //    modal.style.display = "block";
   //}
     
    // 点击 <span> (x), 关闭弹窗
    //span.onclick = function() {
    //    modal.style.display = "none";
    //}
    $('.md-trigger').on('click',function(){
        var modal = $(this).data('modal');
        $("#" + modal).niftyModal();
    });     
    $('#btn_upload').bind('submit', function(e) {
        jQ.ajax({
          'url': url,
          'type': 'GET',
          'data': jQ(this).serialize(),
          'success': function (data, textStatus, jqXHR) {
            container.html(data);
          }
        });
    });
});