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

function getDetailTransaction(e, id){
	e.preventDefault();
	$.ajax({
		url:`http://127.0.0.1:8000/transaction-details/${id}/`,
		type:'POST',
		headers: {
			'X-CSRFToken': getCookie('csrftoken')
        },
		data:{
			'csrfmiddlewaretoken':getCookie('csrftoken')
		},
		success:function(response){
			if(response){
				$('#paymentMethod').text(': BNI');
				// $('#price').text(`:  Rp. ${response.data[0].place}`);
				$('#id').text(`:  ${response.data[0].id}`);
				$('#date').text(`:  ${response.data[0].time}`);
				$('#status').text(`:  ${response.data[0].status}`);
			}
		}

	});

}