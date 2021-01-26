$(function(){
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  $('#search').keyup(function(event){
    event.preventDefault()
    $('#filtered_companies').html('').load(
      "/companies/filter/",
      {
        'search_text': $('#search').val(),
        "csrfmiddlewaretoken": csrftoken
      }
    );
  });

  intern_val = "False"
  place_val = "False"
  all_val = "True"

  $('#all').click(function(){
    if(all_val == "False"){
      all_val = "True"
      intern_val = "False"
      place_val = "False"
      $('#intern').prop("checked", false)
      $('#place').prop("checked", false)
      $('#filtered_companies').html('').load(
        "/companies/ipfilter/",
        {
          'intern_val': intern_val,
          'place_val': place_val,
          'all_val': all_val,
          'csrfmiddlewaretoken': csrftoken
        }
      );
    }
  });

  $('#intern').click(function(){
    if(intern_val == "True") intern_val = "False"
    else intern_val = "True"
    all_val = "False"
    $('#filtered_companies').html('').load(
      "/companies/ipfilter/",
      {
        'intern_val': intern_val,
        'place_val': place_val,
        'all_val': "False",
        "csrfmiddlewaretoken": csrftoken
      }
    );
  });

  $('#place').click(function(){
    if(place_val == "True") place_val = "False"
    else place_val = "True"
    all_val = "False"
    $('#filtered_companies').html('').load(
      "/companies/ipfilter/",
      {
        'intern_val': intern_val,
        'place_val': place_val,
        'all_val': "False",
        "csrfmiddlewaretoken": csrftoken
      }
    );
  });
});
