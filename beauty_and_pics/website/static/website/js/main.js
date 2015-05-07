/*
	The MIT License (MIT)

	Copyright (c) 2015 entpy software

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
*/

$(document).ready(function(){
	$("body").on("click",".navbar-toggle", function(){
		$(".toggle_navigation").toggle();
	});

	// calculate contest start/expiring date
	manageContestTimedelta();

	// write bootstrap modal inside body tag
	bootstrapModalsObect.writeModalInsideBodyTag();
});

// Avoid `console` errors in browsers that lack a console.
(function() {
    var method;
    var noop = function () {};
    var methods = [
        'assert', 'clear', 'count', 'debug', 'dir', 'dirxml', 'error',
        'exception', 'group', 'groupCollapsed', 'groupEnd', 'info', 'log',
        'markTimeline', 'profile', 'profileEnd', 'table', 'time', 'timeEnd',
        'timeStamp', 'trace', 'warn'
    ];
    var length = methods.length;
    var console = (window.console = window.console || {});

    while (length--) {
        method = methods[length];

        // Only stub undefined methods.
        if (!console[method]) {
            console[method] = noop;
        }
    }
}());

/* Function to read csrftoken from cookie */
function readCsrftokenFromCookie() {
	return $.cookie('csrftoken');
}

/* Function to generate a random number */
function randomInt(min, max) {
	return Math.floor(Math.random() * max + min);
}

function getImageTemplateHtml(imageUrl) {
	var imageTemplate = false;
	if (imageUrl) {
		imageTemplate = '<img style="width: 100%;" alt="Image preview" src="' + imageUrl + '">';
	}

	return imageTemplate
}

/* Function to retrieve current timestamp in seconds */
function getCurrentTimestamp() {
	var dateObj = new Date();
	// retrieve timestam in microseconds
	var current_timestamp = dateObj.getTime();

	// return timestam in seconds
	return Math.floor(current_timestamp / 1000);
}

/* Function to manage contest timedelta (run this function every second)*/
function manageContestTimedelta() {
	if ($(".contest_info_block").length) {
		// buld and write timedelta string inside container
		buildAndWriteContestTimedeltaString();
	}
}

/* Function to build contest expiring/start date string */
function buildAndWriteContestTimedeltaString() {
	var contestStatus = $(".contest_info_block").data("contestStatus");
	var timedelta = $(".contest_info_block").data("contestTimeDelta");

	countdown.setLabels(
		' millisecondo| secondo| minuto| ora| giorno| settimana| mese| anno| decennio| secolo| millennio',
		' millisecondi| secondi| minuti| ore| giorni| settimane| mesi| anni| decenni| secoli| millenni',
		' e ',
		'  '
	);

	// countdown launch
	runCountdown(timedelta, contestStatus)

	// print contest status string
	writeCountdownContestStatusString(contestStatus);
}

/* Function to launch a countdown */
function runCountdown(timedelta, contestStatus) {
	if (timedelta && contestStatus) {
		var timerId = countdown(timedelta * 1, function(ts) {
			if (!ts.days && !ts.hours && !ts.minutes && !ts.seconds) {
				// countdown finish
				window.clearInterval(timerId);
				setTimeout(function() { writeCountdownEndString(contestStatus); }, 1100);
			}
			$('.contest_timedelta_string_container').html(ts.toHTML());
		}, countdown.DAYS|countdown.HOURS|countdown.MINUTES|countdown.SECONDS).toString();
	}
}

/* Function to write contest status string */
function writeCountdownContestStatusString(contestStatus) {
	if (contestStatus == "active") {
		$('.contest_status_container').html("alla chiusura del concorso");
	} else if (contestStatus == "opening") {
		$('.contest_status_container').html("all'apertura del concorso");
	}
}

/* Function to write string at the countdown finish */
function writeCountdownEndString(contestStatus) {
	if (contestStatus == "active") {
		$('.contest_timedelta_string_container').html("Il contest è stato appena chiuso!");
		$('.contest_status_container').html("");
	} else if (contestStatus == "opening") {
		$('.contest_timedelta_string_container').html("Il contest è stato appena aperto!");
		$('.contest_status_container').html("");
	}
}

/* Object to manage bootstrap modals */
var bootstrapModalsObect = {

	/* Function to write bootstrap modal inside body tag, only if not already exists */
	writeModalInsideBodyTag: function() {
		if (!$(".bootstrap_modal").length) {
			var bootstrapModal = '';
			bootstrapModal += '<div class="bootstrap_modal modal fade bs-example-modal-lg" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">';
			bootstrapModal += this.getBootstrapModalHtmlTemplate();
			bootstrapModal += '</div>';
			$("body").prepend(bootstrapModal);
		}

		return true;
	},

	/* Function to retrieve bootstrap modal html template */
	getBootstrapModalHtmlTemplate: function() {
		var bootstrapModal = '';
		bootstrapModal += '<div class="modal-dialog">';
		bootstrapModal += '<div class="modal-content">';
		bootstrapModal += '<div class="modal-header">';
		bootstrapModal += '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
		bootstrapModal += '<h4 class="modal-title">&nbsp;</h4>';
		bootstrapModal += '</div>';
		bootstrapModal += '<div class="modal-body">';
		bootstrapModal += '</div>';
		bootstrapModal += '<div class="modal-footer"></div>';
		bootstrapModal += '</div><!-- /.modal-content -->';
		bootstrapModal += '</div><!-- /.modal-dialog -->';

		return bootstrapModal;
	},

	/* Function to reset bootstrap modal */
	resetBootstrapModal: function() {
		$(".bootstrap_modal").html(this.getBootstrapModalHtmlTemplate());
	},

	/* Function to show bootstrap modal */
	showBootstrapModal: function() {
		$(".bootstrap_modal").modal();
	},

	/* Function to hide bootstrap modal */
	hideBootstrapModal: function() {
		$(".bootstrap_modal").hide();
	},

	/* custom bootstrap modal functions {{{ */
	/* Function to build and show image zoom bootstrap modal */
	showZoomImageModal: function(imageUrl) {
		if (imageUrl) {
			this.resetBootstrapModal();
			$(".bootstrap_modal").find('.modal-body').html(this.getImageHtmlBlock(imageUrl));
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show delete image bootstrap modal */
	showDeleteImageModal: function(imageUrl, imageId) {
		if (imageUrl && imageId) {
			this.resetBootstrapModal();
			$(".bootstrap_modal").find('.modal-body').html(this.getImageHtmlBlock(imageUrl));
			$(".bootstrap_modal").find('.modal-footer').html(this.deleteImageButtonHtmlBlock(imageId));
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show perform login bootstrap modal */
	showPerformLoginModal: function() {
		this.resetBootstrapModal();
        performLoginTemplate = "";
        performLoginTemplate += '<div class="container-fluid">';
        performLoginTemplate += '<div class="row">';
        performLoginTemplate += '<div class="col-md-12">';
        performLoginTemplate += '<p>Per poter continuare è necessario accedere.</p>';
        performLoginTemplate += '</div>';
        performLoginTemplate += '<div class="col-md-12">';
        performLoginTemplate += '<a href="/login/" class="btn btn-success">Accedi</a>';
        performLoginTemplate += '</div>';
        performLoginTemplate += '</div>';
        performLoginTemplate += '<div class="row">';
        performLoginTemplate += '<div class="col-md-12 margin_top_30">';
        performLoginTemplate += '<b>Non sei ancora registrato?</b> <a href="/registrati/">Registrati</a> e partecipa al concorso, la prossima star di Beauty & Pics potresti essere tu!</p>';
        performLoginTemplate += '</div>';
        performLoginTemplate += '</div>';
        performLoginTemplate += '</div>';
		$(".bootstrap_modal").find('.modal-title').html("Aggiungi preferito");
		$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
		$(".bootstrap_modal").find('.modal-body').html(performLoginTemplate);
		this.showBootstrapModal();

		return false;
	},

	/* Function to build and show a success bootstrap modal */
	showSuccessModal: function(message) {
		if (message) {
			this.resetBootstrapModal();
            var messageBlockTemplate = '';
            messageBlockTemplate += '<div class="row">';
            messageBlockTemplate += '<div class="col-md-12 margin_top_30">';
            messageBlockTemplate += '<div class="alert alert-info">';
            messageBlockTemplate += message;
            messageBlockTemplate += '</div>';
            messageBlockTemplate += '</div>';
            messageBlockTemplate += '</div>';
            $(".bootstrap_modal").find('.modal-title').html("Ottimo");
            $(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show an alert bootstrap modal */
	showAlertModal: function(message) {
		if (message) {
			this.resetBootstrapModal();
            var messageBlockTemplate = '';
            messageBlockTemplate += '<div class="row">';
            messageBlockTemplate += '<div class="col-md-12 margin_top_30">';
            messageBlockTemplate += '<div class="alert alert-warning">';
            messageBlockTemplate += message;
            messageBlockTemplate += '</div>';
            messageBlockTemplate += '</div>';
            messageBlockTemplate += '</div>';
            $(".bootstrap_modal").find('.modal-title').html("Gulp...");
            $(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},

	/* custom bootstrap modal functions }}} */

	getImageHtmlBlock: function(imageUrl) {
		var templateBlock = false;
		if (imageUrl) {
			templateBlock = '<img style="width: 100%;" alt="Image preview" src="' + imageUrl + '">';
		}

		return templateBlock;
	},

	deleteImageButtonHtmlBlock: function(imageId) {
		var templateBlock = false;
		if (imageId) {
			templateBlock = '<button type="button" data-image-id="' + imageId + '" class="btn btn-success deleteProfileImageClickAction">Cancella</button>';
		}

		return templateBlock;
	}
};

/* Object to perform custom ajax action */
var customAjaxAction = {
	__ajaxCallParams : false,
	__ajaxCallActionName : false,
	__ajaxCallAsync : true,
	__ajaxSuccessCallbackFunction : function() { },
	__ajaxErrorCallbackFunction : function() { },
	ajaxCallUrl : "/ajax/", // the ajax call url

	/* Function to set action name */
	setActionName : function(actionName) {
		if (actionName) {
			this.__ajaxCallActionName = actionName;
		}
	},

	/* Function to retrieve action name */
	getActionName : function() {
		return this.__ajaxCallActionName;
	},

	/* Function to set async flag */
	setAsyncFlag : function(asyncFlag) {
		this.__ajaxCallAsync = asyncFlag;
	},

	/* Function to retrieve async flag */
	getAsyncFlag : function() {
		return this.__ajaxCallAsync;
	},

	/* Function to set a success callback function */
	setAjaxSuccessCallbackFunction : function(callbackFunction) {
		if (callbackFunction) {
			this.__ajaxSuccessCallbackFunction = callbackFunction;
		}
	},

	/* Function to retrieve a success callback function */
	getAjaxSuccessCallbackFunction : function(jsonResponse) {
		return this.__ajaxSuccessCallbackFunction(jsonResponse);
	},

	/* Function to set an error callback function */
	setAjaxErrorCallbackFunction : function(callbackFunction) {
		if (callbackFunction) {
			this.__ajaxErrorCallbackFunction = callbackFunction;
		}
	},

	/* Function to retrieve an error callback function */
	getAjaxErrorCallbackFunction : function(jsonResponse) {
		return this.__ajaxErrorCallbackFunction(jsonResponse);
	},

	/* Function to set ajax call params */
	setAjaxCallParams : function(paramsList) {
		if (paramsList) {
			this.__ajaxCallParams = paramsList;
		}
	},

	/* Function to retrieve ajax call params */
	getAjaxCallParams : function() {
		return this.__ajaxCallParams;
	},

	/* Function to perform an action */
	performAjaxAction : function() {
		// reading csrfmiddlewaretoken from cookie
		var csrftoken = readCsrftokenFromCookie();
		var ajaxCallData = {
			url : this.ajaxCallUrl,
			data : this.getAjaxCallParams() + "&ajax_action=" + this.getActionName(),
			async : this.getAsyncFlag(),
			headers: { "X-CSRFToken": csrftoken },
			success : function(jsonResponse) {
				// functions to manage JSON response
				console.log("==========risultato chiamata==========");
				console.log(jsonResponse);
				if (jsonResponse.success) {
					customAjaxAction.getAjaxSuccessCallbackFunction(jsonResponse);
				} else if (jsonResponse.error) {
					customAjaxAction.getAjaxErrorCallbackFunction(jsonResponse);
				}
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
};

/* Object to perform votes */
var voteUserObject = {
	__ajaxCallParams : {
		"global_vote_points" : null, // point about global vote
		"smile_vote_points" : null, // point about smile vote
		"look_vote_points" : null, // point about look vote
		"user_id" : null, // id account to vote
	},
	globalVoteContainerClass : ".global_vote",
	smileVoteContainerClass : ".smile_vote",
	lookVoteContainerClass : ".look_vote",
	votationBlockErrorClassName : "votation_block_error",
	messageBlockText : "Potrai votare nuovamente questo partecipante quando saranno passate 48 ore dalla tua votazione.",
	messageBlockClass : "msgTextAction",
	messageContainerClass : ".msgContainerAction",
	voteFormContainerClass : ".voteFormContainerAction",
	ajaxCallUrl : "/ajax/", // the ajax call url

	/* Function to add a new AND filter */
	addParam : function(paramName, paramValue) {
		if (paramName) {
			if (!paramValue) paramValue = null
			// retrieve previously added filters
			var existing_params = this.getParamsList();
			// override or add new filter
			existing_params[paramName] = paramValue;
			// setting new filters object
			this.setParamsList(existing_params);
		}

		return true;
	},

	/* Function to set a list of ajax call params */
	setParamsList : function(paramsList) {
		if (paramsList) {
			this.__ajaxCallParams = paramsList
		}

		return true;
	},

	/* Function to retrieve a list of ajax call params */
	getParamsList : function() { return this.__ajaxCallParams; },

	/* Function to check if all votes were done */
	checkVoteActionErrors : function() {
		var returnVar = true;
		var existing_params = this.getParamsList();

		// global votation check {{{
		if (existing_params["global_vote_points"]) {
			this.removeGlobalTypeError();
		} else {
			this.showGlobalTypeError();
			returnVar = false;
		}
		// global votation check }}}
		// smile votation check {{{
		if (existing_params["smile_vote_points"]) {
			this.removeSmileTypeError();
		} else {
			this.showSmileTypeError();
			returnVar = false;
		}
		// smile votation check }}}
		// look votation check {{{
		if (existing_params["look_vote_points"]) {
			this.removeLookTypeError();
		} else {
			this.showLookTypeError();
			returnVar = false;
		}
		// look votation check }}}

		if (!returnVar) {
			// alert("Per poter votare devi esprimere un giudizio su ogni metrica!");
		} else if (!confirm("Confermi il voto? Potrai ri-votare questa persona tra 48 ore!")) {
				returnVar = false;
		}

		// user_id check {{{
		if (!existing_params["user_id"]) {
			console.log("errore inaspettato, user_id non settato, contattare l'amministratore.");
			returnVar = false;
		}
		// user_id check }}}

		return returnVar;
	},

	// Function to add error class to votation block
	showGlobalTypeError : function() { $(this.globalVoteContainerClass).addClass(this.votationBlockErrorClassName); },
	showSmileTypeError : function() { $(this.smileVoteContainerClass).addClass(this.votationBlockErrorClassName); },
	showLookTypeError : function() { $(this.lookVoteContainerClass).addClass(this.votationBlockErrorClassName); },

	// Function to remove error class to votation block
	removeGlobalTypeError : function() { $(this.globalVoteContainerClass).removeClass(this.votationBlockErrorClassName); },
	removeSmileTypeError : function() { $(this.smileVoteContainerClass).removeClass(this.votationBlockErrorClassName); },
	removeLookTypeError : function() { $(this.lookVoteContainerClass).removeClass(this.votationBlockErrorClassName); },

	/* Function to perform a votation */
	performVotingAction : function() {
		if (this.checkVoteActionErrors()) {
			// reading csrfmiddlewaretoken from cookie
			var csrftoken = readCsrftokenFromCookie();
			var ajaxCallData = {
				url : this.ajaxCallUrl,
				data : $.param(this.getParamsList()) + "&ajax_action=perform_voting",
				async : true,
				headers: { "X-CSRFToken": csrftoken },
				success : function(jsonResponse) {
					// functions to manage JSON response
					console.log("==========risultato chiamata==========");
					console.log(jsonResponse);
					if (jsonResponse.success) {
						voteUserObject.successVotingAction(jsonResponse.message)
					} else if (jsonResponse.error) {
						voteUserObject.errorVotingAction(jsonResponse.message)
					}
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

	errorVotingAction : function(message) {
		// show error messages
		alert(message);
	},

	successVotingAction : function(message) {
		// show success messages
		alert(message);
		$(this.messageBlockClass).html(this.messageBlockText);
		$(this.messageContainerClass).removeClass("hide");

		// hide vote form
		$(this.voteFormContainerClass).addClass("hide");
	},
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

	/* Function to reset all filters */
	__resetFilters : function() {
		this.__elementsListFilters["user_id"] = null;
		this.__elementsListFilters["elements_list_type"] = null;
		this.__elementsListFilters["start_limit"] = 0;
		this.__elementsListFilters["show_limit"] = 1;
		this.__elementsListFilters["filter_name"] = null;
	},

	/* Function to clear current loaded elements inside html */
	__clearHtml : function() {
		$(this.blocksContainerClassName).html("");
	},

	/* Function to clear current element list */
	newElementList : function() {
		this.__resetFilters();
		this.__clearHtml();
		this.showActionButton();
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

	showActionButton : function() {
	/* Function to show action button */
		$(this.actionButtonClassName).show();
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
			blockThumbnailImageUrl = singleElement.thumbnail_image_url;
			items += elementsListObject.getSingleHtmlBlock(blockUrl, blockThumbnailImageUrl);
		});

		// return jQuery object
		return $(items);
	},

	manageFavoriteList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(index, singleElement) {
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
		$.each(elementsList, function(index, singleElement) {
			blockUrl = "#";
			// alert(singleElement.image_url);
			blockThumbnailImageUrl = singleElement.thumbnail_image_url;
			blockImageUrl = singleElement.image_url;
			blockImageId = singleElement.image_id;
			items += elementsListObject.getSingleHtmlBlock(blockUrl, blockThumbnailImageUrl, blockImageUrl, "zoom-image", blockImageId);
		});

		// return jQuery object
		return $(items);
	},

	getSingleHtmlBlock : function(blockUrl, blockThumbnailImageUrl, blockImageUrl, imgTagClass, imgId) {

		returnVar = "";
		if (!imgTagClass) {
			imgTagClass = "";
		}

		if (!imgId) {
			imgId = "";
		}

		if (blockUrl && blockThumbnailImageUrl) {
			// setting bootstrap block size
			if (!this.bootstrapBlockSize) {
				this.bootstrapBlockSize = true;
			}
			var lg_size = (this.bootstrapBlockSize["lg_size"] ? this.bootstrapBlockSize["lg_size"] : "15");
			var md_size = (this.bootstrapBlockSize["md_size"] ? this.bootstrapBlockSize["md_size"] : "3");
			var sm_size = (this.bootstrapBlockSize["sm_size"] ? this.bootstrapBlockSize["sm_size"] : "3");
			var xs_size = (this.bootstrapBlockSize["xs_size"] ? this.bootstrapBlockSize["xs_size"] : "6");
			// build html block with link and image
			var returnVar = '<div class="col-lg-' + lg_size + ' col-md-' + md_size + ' col-xs-' + xs_size + ' col-sm-' + sm_size + ' thumb imgBlockContainer_' + imgId + '"><a href="' + blockUrl + '" class="thumbnail"><img alt="" src="' + blockThumbnailImageUrl + '" data-fullimage-url="' + blockImageUrl + '" data-image-id="' + imgId + '" class="img-responsive ' + imgTagClass + '"></a></div>'
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
