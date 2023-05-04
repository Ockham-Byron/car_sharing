

jQuery(document).ready(function($) {

	
function open_modal(url) {
	$('#show_modal').load(url, function () {
		$(this).modal('show');
	});
}


function close_modal(){
	$('#modal').modal('hide');
}


})
