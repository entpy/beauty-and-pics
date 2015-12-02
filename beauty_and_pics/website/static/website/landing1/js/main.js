$(document).ready(function() {
	$(window).load(function(){
		// $('.page-loader').fadeOut('slow');
	});

	wow = new WOW({
		animateClass: 'animated',
		mobile: false,
		offset: 70
	});
	wow.init();
});
