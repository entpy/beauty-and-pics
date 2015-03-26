$(document).ready(function(){
	$(".navbar-toggle").on("click", function(){
		$(".toggle_navigation").toggle();
	});
});

function randomInt(min, max) {
	return Math.floor(Math.random() * max + min);
}

/*
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
*/

function getItems(block_size) {
	var items = '';
	for ( var i=0; i < 12; i++ ) {
		items += getItem(block_size);
	}

	// return jQuery object
	return $(items);
}

/* Object to retrieve a filtered list of elements (user or photo book) */
var elementsListObject = {
	__startLimit : 0, // element retrieving start limit
	__showLimit : 10, // number of element retrieved per call
	__elementsListFilters : {
		"user_id" : null, // required in "favorites" and "book" elementsListType
		"elements_list_type" : null, // catwalker, favorite, photobook
	}, // list of AND filters */
	ajaxCallUrl : "/ajax/", // the ajax call url
	bootstrapBlockSize : null, // the bootstrap block size for display
	blocksContainerClassName : ".image_grid_container", // the block container class inside html page

	/* Function to read csrftoken from cookie */
	readCsrftokenFromCookie : function() {
		return $.cookie('csrftoken');
	},

	/* Function to add a new AND filter */
	addFilter : function(filterName, filterValue) {
		if (filterName) {
			if (!filterValue) filterValue = null
			// retrieve previously added filters
			var existing_filters = this.getElementsListFilters();
			// override or add new filter
			existing_filters[filterName] = filterValue;
			// setting new filters object
			this.setElementsListFilters(existing_filters);
		}

		return true;
	},

	/* Function to set list of AND filters */
	setElementsListFilters : function(elementsListFilters) {
		if (elementsListFilters) {
			this.__elementsListFilters = elementsListFilters
		}

		return true;
	},

	/* Function to retrieve list of AND filters */
	getElementsListFilters : function() { return this.__elementsListFilters; },

	/* Function to set element start limit */
	setStartLimit : function(startLimit) {
		if (startLimit) {
			this.__startLimit = startLimit
		}

		return true;
	},

	/* Function to set element show limit */
	setShowLimit : function(showLimit) {
		if (showLimit) {
			this.__showLimit = showLimit
		}

		return true;
	},

	/* Function to set user id */
	setUserId : function(userId) {
		if (userId) {
			// retrieve previously added filters
			var existing_filters = this.getElementsListFilters();
			existing_filters["userId"] = userId;
			// setting new filters object
			this.setElementsListFilters(existing_filters);
		}

		return true;
	},

	/* Function to set elements list type */
	setElementsListType : function(elementsListType) {
		if (elementsListType) {
			// retrieve previously added filters
			var existing_filters = this.getElementsListFilters();
			existing_filters["elementsListType"] = elementsListType;
			// setting new filters object
			this.setElementsListFilters(existing_filters);
		}

		return true;
	},

	/* Function to retrieve element start limit */
	getStartLimit : function() { return this.__startLimit; },

	/* Function to retrieve number of elements per call */
	getShowLimit : function() { return this.__showLimit; },

	/* Function to retrieve user id */
	getUserId : function() { return this.__userId; },

	/* Function to retrieve elements list type */
	getElementsListType : function() { return this.__elementsListType; },

	getElementsList : function() {
		// reading csrfmiddlewaretoken from cookie
		var csrftoken = this.readCsrftokenFromCookie();
		var ajaxCallData = {
			url : this.ajaxCallUrl,
			data : JSON.stringify(this.getElementsListFilters()) + "&ajax_action=elements_list",
			async : true,
			headers: { "X-CSRFToken": csrftoken },
			success : function(jsonResponse) {
				// funzioni (utenti passerella, preferiti e immagini)
				// per gestire i valori di ritorno della suddetta funzione!!
				// functions to manage JSON response
				console.log(jsonResponse);
				if (jsonResponse.elements_list_type == "catwalker") {
					// build and write block into html
					this.writeHtmlBlock(this.manageCatwalkerList(jsonResponse.elements_list));
				} else if (jsonResponse.elements_list_type == "favorite") {
					// build and write block into html
					this.writeHtmlBlock(this.manageFavoriteList(jsonResponse.elements_list));
				} else if (jsonResponse.elements_list_type == "photobook") {
					// build and write block into html
					this.writeHtmlBlock(this.managePhotobookList(jsonResponse.elements_list));
				}

				// todo: set blocks number limit
				this.setBlocksNumberLimit();
			},
			error : function(jsonResponse) {
				// ...fuck
				// console.log(jsonResponse);
			}
		}

		// performing ajax call
		loadDataWrapper.performAjaxCall(ajaxCallData);

		return true;
	},

	setBlocksNumberLimit : function() {
	/* Function to set block number limit */
		var startLimit = this.getStartLimit() + this.getShowLimit();
		this.setStartLimit(startLimit);
		this.addFilter("start_limit", startLimit);
		this.addFilter("show_limit", this.getShowLimit());
	},

	manageCatwalkerList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(singleElement) {
			blockUrl = "passerella/dettaglio-utente/" + singleElement.user_id;
			blockImageUrl = singleElement.image_url;
			items += this.getSingleHtmlBlock(blockUrl, blockImageUrl);
		}

		// return jQuery object
		return $(items);
	},

	manageFavoriteList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(singleElement) {
			blockUrl = "passerella/dettaglio-utente/" + singleElement.user_id;
			blockImageUrl = singleElement.image_url;
			items += this.getSingleHtmlBlock(blockUrl, blockImageUrl);
		}

		// return jQuery object
		return $(items);
	},

	managePhotobookList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(singleElement) {
			blockUrl = "passerella/dettaglio-utente/" + singleElement.user_id;
			blockImageUrl = singleElement.image_url;
			items += this.getSingleHtmlBlock(blockUrl, blockImageUrl);
		}

		// return jQuery object
		return $(items);
	},

	getSingleHtmlBlock : function(blockUrl, blockImageUrl) {

		returnVar = "";

		if (blockUrl && blockImageUrl) {
			// setting bootstrap block size
			if (!this.bootstrapBlockSize) {
				this.bootstrapBlockSize = true;
			}
			var lg_size = (this.bootstrapBlockSize["lg_size"] ? this.bootstrapBlockSize["lg_size"] : "15");
			var md_size = (this.bootstrapBlockSize["md_size"] ? this.bootstrapBlockSize["md_size"] : "3");
			var sm_size = (this.bootstrapBlockSize["sm_size"] ? this.bootstrapBlockSize["sm_size"] : "3");
			var xs_size = (this.bootstrapBlockSize["xs_size"] ? this.bootstrapBlockSize["xs_size"] : "6");
			// build html block with link and image
			var returnVar = '<div class="col-lg-' + lg_size + ' col-md-' + md_size + ' col-xs-' + xs_size + ' col-sm-' + sm_size + ' thumb"><a href="' + blockUrl + '" class="thumbnail"><img alt="" src="' + blockImageUrl + '" class="img-responsive"></a></div>'
		}

		return returnVar;
	},

	writeHtmlBlock : function(htmlBlocksList) {
	/* function to append blocks into html container */
		// console.log(htmlBlocksList);
		// alert("blocchi 'scritti' con successo");
		$(this.blocksContainerClassName).append(htmlBlocksList);
	},
};

/* Object to manage form errors and success redirect */
var ajaxFormValidation = {

	formClassName : 'ajax_form', // Default "ajax_form"
	errorMessageBoxClassName : 'error_container', // Default "error_container"
	serverMsgContainer : 'server_msg_container', // Server side message container class name
	errorClassName : 'has-error', // Default "has-error"
	formGroupClassName : 'form-group', // Default "form-group"
	// redirectUrl : '', // Es . "/registrati/" Default None
	ajaxCallUrl : "/ajax/", // the ajax call url
	callData : Array(),

	/* Function to read csrftoken from cookie */
	readCsrftokenFromCookie : function() {
		return $.cookie('csrftoken');
	},

	/* Function to manage Ajax form response */
	manageFormResponse : function(jsonResponse) {
		try {
			if (!$.isEmptyObject(jsonResponse)) {
				JSONResult = $.parseJSON(JSON.stringify(jsonResponse));
				if (JSONResult["error"]) {
					this.removeFormErrors();
					this.showFormErrorMessages(JSONResult);
				} else if (JSONResult["success"]) {
					// console.log("Form salvato con successo");
					// submit current form after successfully validation
					this.submitForm();
				}
			}
		} catch(Exception) {
		    // ops...ajax resonse may be corrupted
		    console.log("manageFormErrorResponse error: " + Exception);
		} 
		return true;
	},

	/* Function to submit current form after successfully validation */
	submitForm : function() {
		$("." + this.formClassName).submit();
		return true;
	},

	/* Function to remove all previously errors messagges */
	removeFormErrors : function() {
		$("." + this.formGroupClassName).removeClass(this.errorClassName);
		$("." + this.errorMessageBoxClassName).html("");
		$("." + this.serverMsgContainer).html("");
		return true;
	},

	/* Function to show form error message after Ajax call */
	showFormErrorMessages : function(jsonResponse) {
		if (!$.isEmptyObject(jsonResponse)) {
			$.each(jsonResponse["form_data"], function(fieldName, errorList) {
				if (fieldName == "__all__") {
					ajaxFormValidation.showAllFieldErrorsBox(errorList);
				} else {
					ajaxFormValidation.addSingleFieldErrorClass(fieldName);
				}
			});
		}
		return true;
	},

	/* Function to show a box with main form validation error */
	showAllFieldErrorsBox : function(errorListJson) {
		var errorList = '';
		var htmlErrorBoxTemplate = '';

		$.each(errorListJson, function(field_name, field_errors) {
			errorList += "<li>" + field_errors["message"] + "</li>";
		});

		if (errorList) {
			htmlErrorBoxTemplate += '<div class="row">';
			htmlErrorBoxTemplate += '<div class="col-md-12">';
			htmlErrorBoxTemplate += '<div class="alert alert-danger">';
			htmlErrorBoxTemplate += '<h4>Uhm qualcosa non va!</h4>';
			htmlErrorBoxTemplate += '<ul>';
			htmlErrorBoxTemplate += errorList;
			htmlErrorBoxTemplate += '</ul>';
			htmlErrorBoxTemplate += '</div>';
			htmlErrorBoxTemplate += '</div>';
			htmlErrorBoxTemplate += '</div>';

			$("." + this.errorMessageBoxClassName).html(htmlErrorBoxTemplate);
		}
		return true;
	},

	/* Function to show error on single fields */
	addSingleFieldErrorClass : function(fieldName) {
		$("#id_" + fieldName).parents("." + this.formGroupClassName).addClass(this.errorClassName);
		return true;
	},

	/* Function to check if ajax call can be performed */
	ajaxCallCanBePerformed : function() {
		var returnVar = false;
		if (typeof this.callData !== 'undefined') {
			if (this.ajaxCallUrl && this.callData["data"]) {
				returnVar = true;
			}
		}
		return returnVar;
	},

	/* Function to send form data via Ajax */
	validateForm : function(){
		// check if ajax call can be performed
		if (this.ajaxCallCanBePerformed()) {
			// reading csrfmiddlewaretoken from cookie
			var csrftoken = this.readCsrftokenFromCookie();
			var ajaxCallData = {
				url : this.ajaxCallUrl,
				data : this.callData["data"] + "&ajax_action=form_validation",
				async : true,
				headers: { "X-CSRFToken": csrftoken },
				success : function(jsonResponse) {
					// function to manage JSON response
					// console.log(result);
					ajaxFormValidation.manageFormResponse(jsonResponse);
				},
				error : function(jsonResponse) {
					// ...fuck
					// console.log(jsonResponse);
				}
			}

			// performing ajax call
			loadDataWrapper.performAjaxCall(ajaxCallData);
		}
		return true;
	},
};
