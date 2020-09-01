$(function(){
    $('#search').keyup(function(){
        $.ajax({
            type:"POST",
            url:"/companies/2020",
            data:{
                'search_text': $('#search').val(),
                'csrfmiddleewaretoken': $("input[name=csrfmiddletoken]").val()
            },
            success : searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data,textStatus, jqXHR)
{
    $('#search-list').html(data);
}