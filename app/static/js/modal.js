/*$(document).on('click', '.predict', function(){  // Кнопка редактирования
    $.ajax({
        url:"/",
        method:"POST",
        data:{text:text},
        dataType:"json",
        success:function(data)
        {
            $('#exampleModal').modal('show');   // показываем имеющиеся значения
            $('#text').val(data.text);
            $('#class').val(data.class);
            $('#lemmas').val(data.lemmas);
            $('#scores').val(data.scores);
        }
    })
});

$.ajax({
    url: '/',
    method: 'POST',
    dataType: 'json',
    success: function(data){
        alert(data.text);
        alert(data.error);
    }
});
*/