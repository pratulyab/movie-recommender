<script>

$(document).ready(function(){
	$('select').material_select(); // initialize the select dropdowns
	//Search
	var typingTimer;
	var doneTypingInterval = 300;
	var $input = $('#search');
	var $results = $('#search-results');
	var a_mousedown = false;

	//on keyup, start the countdown
	$input.on('keyup', function () {
		clearTimeout(typingTimer);
		typingTimer = setTimeout(search, doneTypingInterval);
	});

//on keydown, clear the countdown 
	$input.on('keydown', function () {
		clearTimeout(typingTimer);
	});

	$input.on('blur', function(e) {
		if (!a_mousedown)
			$results.css("display", "none");
		else
			a_mousedown = false;
	});


	$input.on('focus', function() {
		$results.css("display", "block");
	});
	
	function search (){
		var $form = $('#search-form'),
			url = $form.attr('action'),
			query = $input.val(),
			type = $form.attr('method');
		$.ajax({
			url: url,
			type: type,
			data: {'query': query},
			processData: true,
			contentType: false,
			beforeSend: function() {
				Materialize.toast('<b class="yellow-text">Fetching Results...</b>', 10000);
			},
			complete: function() {
				$('.toast').remove();
				Materialize.toast('<b class="yellow-text">Results Loaded.</b>', 1000);
			},
			success: function(data, status, xhr){
				if (!data.result)
					$results.html("<p class='center'>"+data.message+"</p>")
				else {
					var $ul = $('<ul class="col s12 teal-text"/>');
					for (var each of data.result) {
						var $li = $('<li class="col s12"/>'),
							$a = $('<a class="result-link"/>');
						$a.attr('href', each.url);
						$a.text(each.name);
						$ul.append($li.append($a));
					}
					$results.empty();
					$results.append($ul);
					$('.result-link').mousedown(function(e){a_mousedown=true;});
				}
				$results.css("display", "block");
			},
			error: function(status, xhr, error){
				if (status.status >= 500)
					Materialize.toast('<b class="red-text">Sorry, unexpected error occurred. Please try again later.</b>', 4000);
				else
					Materialize.toast(('<b class="red-text">' + (xhr['error'] ? xhr['error'] : 'Sorry, an error occurred.') + '</b>'), 4000);
			},
		});
	}

	$('#genre-form').on('submit', function(e){
		e.preventDefault();
		var $form = $(this),
			url = $(this).attr('action'),
			type = $(this).attr('method'),
			form_data = new FormData($form[0]);
		$.ajax({
			url: url,
			type: type,
			data: form_data,
			processData: false,
			contentType: false,
			beforeSend: function() {
				$('#genre-preloader').html($('<div class="progress"><div class="indeterminate"></div></div>'));
				$('#genre-recommendations').empty();
			},
			complete: function() {
				$('#genre-preloader').empty();
			},
			success: function(data, status, xhr){
				$('#genre-recommendations').html(data.html);
			},
			error: function(status, xhr, error){
				if (status.status >= 500)
					Materialize.toast('<b class="red-text">Sorry, unexpected error occurred. Please try again later.</b>', 4000);
				else
					Materialize.toast(('<b class="red-text">' + (xhr['error'] ? xhr['error'] : 'Sorry, an error occurred.') + '</b>'), 4000);
			},
		});
	});
});
</script>

