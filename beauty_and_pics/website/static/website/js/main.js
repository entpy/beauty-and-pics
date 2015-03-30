/**
 * 	Author: Entpy Software <developer at entpy dot com>
 * 	Version: 0.1.0
 *
 * 	License: GPL_v3 {Link: http://gplv3.fsf.org/}
 *
 *	Permission is hereby granted, free of charge, to any person obtaining
 *	a copy of this software and associated documentation files (the
 *	"Software"), to deal in the Software without restriction, including
 *	without limitation the rights to use, copy, modify, merge, publish,
 *	distribute, sublicense, and/or sell copies of the Software, and to
 *	permit persons to whom the Software is furnished to do so, subject to
 *	the following conditions:
 *
 *	The above copyright notice and this permission notice shall be
 *	included in all copies or substantial portions of the Software.
 *
 *	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 *	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 *	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 *      NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 *      LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 *      OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 *      WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

$(document).ready(function(){
	$(".navbar-toggle").on("click", function(){
		$(".toggle_navigation").toggle();
	});
});

/* Function to read csrftoken from cookie */
readCsrftokenFromCookie : function() {
	return $.cookie('csrftoken');
},

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


function getItems(block_size) {
	var items = '';
	for ( var i=0; i < 12; i++ ) {
		items += getItem(block_size);
	}

	// return jQuery object
	return $(items);
}*/

/* Object to perform votes */
var voteUserObject = {
	__ajaxCallParams : {
		"global_vote_points" : null, // point about global vote
		"face_vote_points" : null, // point about face vote
		"look_vote_points" : null, // point about look vote
		"id_user" : null, // id account to vote
	},
	globalVoteContainerClass : ".global_vote",
	faceVoteContainerClass : ".face_vote",
	lookVoteContainerClass : ".look_vote",
	votationBlockErrorClassName : "votation_block_error",
	ajaxCallUrl : "/ajax/", // the ajax call url

	// ajax call params setter
	setGlobalVotePoints : function(points) { if (points) { this.__ajaxCallParams["global_vote_points"] = points; } },
	setFaceVotePoints : function(points) { if (points) { this.__ajaxCallParams["face_vote_points"] = points; } },
	setLookVotePoints : function(points) { if (points) { this.__ajaxCallParams["look_vote_points"] = points; } },
	setIdUser : function(idUser) { if (idUser) { this.__ajaxCallParams["id_user"] = idUser; } },

	// ajax call params getter
	getGlobalVotePoints : function() { return this.__ajaxCallParams["global_vote_points"]; },
	getFaceVotePoints : function() { return this.__ajaxCallParams["face_vote_points"]; },
	getLookVotePoints : function() { return this.__ajaxCallParams["look_vote_points"]; },
	getIdUser : function() { return this.__ajaxCallParams["id_user"]; },

	/* function to check if all votes were done */
	checkAllVoteAreSet : function() {
		var returnVar = true;
		// global votation check {{{
		if (this.getGlobalVotePoints()) {
			this.removeGlobalTypeError();
		} else {
			this.showGlobalTypeError();
			returnVar = false;
		}
		// global votation check }}}
		// face votation check {{{
		if (this.getFaceVotePoints()) {
			this.removeFaceTypeError();
		} else {
			this.showFaceTypeError();
			returnVar = false;
		}
		// face votation check }}}
		// look votation check {{{
		if (this.getLookVotePoints()) {
			this.removeLookTypeError();
		} else {
			this.showLookTypeError();
			returnVar = false;
		}
		// look votation check }}}

		return returnVar;
	},

	// function to add error class to votation block
	showGlobalTypeError : function() { $(this.globalVoteContainerClass).addClass(this.votationBlockErrorClassName); },
	showFaceTypeError : function() { $(this.faceVoteContainerClass).addClass(this.votationBlockErrorClassName); },
	showLookTypeError : function() { $(this.getLookVotePoints).addClass(this.votationBlockErrorClassName); },

	// function to remove error class to votation block
	removeGlobalTypeError : function() { $(this.globalVoteContainerClass).removeClass(this.votationBlockErrorClassName); },
	removeFaceTypeError : function() { $(this.faceVoteContainerClass).removeClass(this.votationBlockErrorClassName); },
	removeLookTypeError : function() { $(this.getLookVotePoints).removeClass(this.votationBlockErrorClassName); },

	/* function to perfor a votation */
	performVotingAction : function() {
		if (this.checkAllVoteAreSet()) {
			// reading csrfmiddlewaretoken from cookie
			var csrftoken = readCsrftokenFromCookie();
			var ajaxCallData = {
				url : this.ajaxCallUrl,
				data : $.param(this.__ajaxCallParams()) + "&ajax_action=perform_voting",
				async : true,
				headers: { "X-CSRFToken": csrftoken },
				success : function(jsonResponse) {
					// functions to manage JSON response
					console.log("==========risultato chiamata==========");
					console.log(jsonResponse);
				},
				error : function(jsonResponse) {
					// ...fuck
					// console.log(jsonResponse);
				}
			}
		}
	},

	errorVotingAction : function() { return true; },

	successVotingAction : function() { return true; },
};

/* Object to retrieve a filtered list of elements (user or photo book) */
var elementsListObject = {
	__elementsListFilters : {
		"user_id" : null, // required in "favorites" and "book" elementsListType
		"elements_list_type" : null, // catwalker, favorite, photobook
		"start_limit" : 0, // element retrieving start limit
		"show_limit" : 1, // number of element retrieved per call
		"filter_name" : null, // main filter (Es. latest_registered, classification, ecc...)
	}, // list of AND filters */
	ajaxCallUrl : "/ajax/", // the ajax call url
	bootstrapBlockSize : null, // the bootstrap block size for display
	blocksContainerClassName : ".image_grid_container", // the block container class inside html page
	actionButtonClassName : ".loadMoreElementsAction", // load more button class name

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
			// retrieve previously added filters
			var existing_filters = this.getElementsListFilters();
			existing_filters["start_limit"] = showLimit;
			// setting new filters object
			this.setElementsListFilters(existing_filters);
		}

		return true;
	},

	/* Function to set element show limit */
	setShowLimit : function(showLimit) {
		if (showLimit) {
			// retrieve previously added filters
			var existing_filters = this.getElementsListFilters();
			existing_filters["show_limit"] = showLimit;
			// setting new filters object
			this.setElementsListFilters(existing_filters);
		}

		return true;
	},

	/* Function to set user id */
	setUserId : function(userId) {
		if (userId) {
			// retrieve previously added filters
			var existing_filters = this.getElementsListFilters();
			existing_filters["user_id"] = userId;
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
			existing_filters["elements_list_type"] = elementsListType;
			// setting new filters object
			this.setElementsListFilters(existing_filters);
		}

		return true;
	},

	getElementsList : function() {
		// reading csrfmiddlewaretoken from cookie
		var csrftoken = readCsrftokenFromCookie();
		var ajaxCallData = {
			url : this.ajaxCallUrl,
			data : $.param(this.getElementsListFilters()) + "&ajax_action=elements_list",
			async : true,
			headers: { "X-CSRFToken": csrftoken },
			success : function(jsonResponse) {
				// functions to manage JSON response
				console.log("==========risultato chiamata==========");
				console.log(jsonResponse);

				// hide show more elements button
				if (jsonResponse.elements_list.length == 0) {
					// TODO: in teoria il pulsante andrebbe nascosto al
					//	 al giro prima!
					elementsListObject.hideActionButton();
				}

				if (jsonResponse.elements_list_type == "catwalker") {
					// build and write block into html
					elementsListObject.writeHtmlBlock(elementsListObject.manageCatwalkerList(jsonResponse.elements_list));
				} else if (jsonResponse.elements_list_type == "favorite") {
					// build and write block into html
					elementsListObject.writeHtmlBlock(elementsListObject.manageFavoriteList(jsonResponse.elements_list));
				} else if (jsonResponse.elements_list_type == "photobook") {
					// build and write block into html
					elementsListObject.writeHtmlBlock(elementsListObject.managePhotobookList(jsonResponse.elements_list));
				}

				// set blocks number limit
				elementsListObject.setBlocksNumberLimit();
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

	hideActionButton : function() {
	/* Function to hide action button */
		$(this.actionButtonClassName).hide();
	},

	setBlocksNumberLimit : function() {
	/* Function to set block number limit */
	/*
	3....8
	9....14
	15....20
	*/

		// retrieve previously added filters
		var existing_filters = this.getElementsListFilters();
		var limit_metric = existing_filters["show_limit"] - existing_filters["start_limit"]
		existing_filters["start_limit"] = existing_filters["show_limit"];
		existing_filters["show_limit"] = existing_filters["start_limit"] + limit_metric;
		// setting new filters object
		this.setElementsListFilters(existing_filters);
	},

	manageCatwalkerList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(index, singleElement) {
			blockUrl = "/passerella/dettaglio-utente/" + singleElement.user_id;
			blockImageUrl = singleElement.image_url;
			items += elementsListObject.getSingleHtmlBlock(blockUrl, blockImageUrl);
		});

		// return jQuery object
		return $(items);
	},

	manageFavoriteList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(singleElement) {
			blockUrl = "passerella/dettaglio-utente/" + singleElement.user_id;
			blockImageUrl = singleElement.image_url;
			items += elementsListObject.getSingleHtmlBlock(blockUrl, blockImageUrl);
		});

		// return jQuery object
		return $(items);
	},

	managePhotobookList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(singleElement) {
			blockUrl = "passerella/dettaglio-utente/" + singleElement.user_id;
			blockImageUrl = singleElement.image_url;
			items += elementsListObject.getSingleHtmlBlock(blockUrl, blockImageUrl);
		});

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
		// alert("blocchi 'scritti' con successo" + this.blocksContainerClassName);
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
			var csrftoken = readCsrftokenFromCookie();
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
