$(document).ready(function(){
	$(".navbar-toggle").on("click", function(){
		$(".toggle_navigation").toggle();
	});
});

/*$.fn.masonryImagesReveal = function($items) {
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
};*/

function randomInt(min, max) {
	return Math.floor(Math.random() * max + min);
}

function getItem(block_size) {

	if (typeof block_size === 'undefined') {
		block_size = true;
	}

	// setting bootstrap block size
	var lg_size = (block_size["lg_size"] ? block_size["lg_size"] : "15");
	var md_size = (block_size["md_size"] ? block_size["md_size"] : "3");
	var sm_size = (block_size["sm_size"] ? block_size["sm_size"] : "3");
	var xs_size = (block_size["xs_size"] ? block_size["xs_size"] : "6");
	var format = randomInt(150, 250);
	var width = format;
	var height = format;
	var item = '<div class="col-lg-' + lg_size + ' col-md-' + md_size + ' col-xs-' + xs_size + ' col-sm-' + sm_size + ' thumb"><a href="#" class="thumbnail"><img alt="" src="http://lorempixel.com/' + width + '/' + height + '/nature" class="img-responsive"></a></div>'

	return item;
}

function getItems(block_size) {
	var items = '';
	for ( var i=0; i < 12; i++ ) {
		items += getItem(block_size);
	}

	// return jQuery object
	return $(items);
}
