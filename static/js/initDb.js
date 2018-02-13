$(function(){
	$('#btnInitDb').click(function(){
		
		$.ajax({
			url: '/initDb',
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});