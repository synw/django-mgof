function fire_request(container_id, url) { 
    var container = '#'+container_id;
	$(container).html('<i class="gus pull-right fa fa-spinner fa-spin"></i>');
	$.ajax({
		type: "GET",
		dataType: "html",
		url: url,
		success: function (content) {
			$(container).html(content);
			},
		error: function(xhr, textStatus, errorThrown) {
	        console.log("Error: "+errorThrown+xhr.status+xhr.responseText);
	        }
    	});
	}
