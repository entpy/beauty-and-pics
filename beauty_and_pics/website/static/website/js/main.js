$(document).ready(function(){
	$(".navbar-toggle").on("click", function(){
		$(".toggle_navigation").toggle();
	});
});

$.fn.masonryImagesReveal = function($items) {
	var msnry = this.data('masonry');
	var itemSelector = msnry.options.itemSelector;
	// hide by default
	$items.hide();
	// append to container
	this.append($items);
	$items.imagesLoaded().progress(function(imgLoad, image) {
		// get item
		// image is imagesLoaded class, not <img>, <img> is image.img
		var $item = $(image.img).parents(itemSelector);
		// un-hide item
		$item.show();
		// masonry does its thing
		msnry.appended($item);
	});

	return this;
};

function randomInt(min, max) {
	return Math.floor(Math.random() * max + min);
}

function getItem() {
	var format = randomInt(150, 250);
	var width = format;
	var height = format;
	var item = '<div class="item"><img src="http://lorempixel.com/' + width + '/' + height + '/nature" /></div>';
	return item;
}

function getItems() {
	var items = '';
	for ( var i=0; i < 12; i++ ) {
		items += getItem();
	}

	// return jQuery object
	return $(items);
}
