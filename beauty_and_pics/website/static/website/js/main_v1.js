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
var scroll_position = false;
var return_position = false;
var not_scroll = false;
$(document).ready(function(){
	// calculate contest start/expiring date
	manageContestTimedelta();

	// write bootstrap modal inside body tag
	bootstrapModalsObect.writeModalInsideBodyTag();

	// show fucking cookie bar (W EU)
	lawCookieCompliance.createDivOnLoad();

	// toggle navigation
	$(document).on("click",".navbar-toggle", function(){
		$(".toggle_navigation").toggle();
	});

	// modal in fase di apertura ma non ancora aperta
	$(document).on('show.bs.modal', ".modal", function () {
		if ($(".modal").css('position') === 'absolute' && !not_scroll) {
			/* We will need to return to where we were.*/
			// return_position = true;
			// saving position
			scroll_position = $(window).scrollTop(); // Where did we start in the window.
			not_scroll = true;
		}
	});

	// modal apertura completata
	$(document).on('shown.bs.modal', ".modal", function () {
		if ($(".modal").css('position') === 'absolute') {
			// scroll top page top
			$(window).scrollTop(0);
		}
	});

	// modal in fase di chiusura ma non ancora chiusa
	$(document).on('hide.bs.modal', ".modal", function (e) {
		if ($(".modal").css('position') === 'absolute') {
			/* Return to where we were.*/
			$(window).scrollTop(scroll_position);
			not_scroll = false;
		}
	});

	/* open modal to resend email confirmation */
	$(document).on("click",".openResendConfirmationModalClickAction", function(){
		bootstrapModalsObect.showSendValidationEmail();

		return false;
	});

	/* function to resend a confirmation email */
	$(document).on("click",".resendConfirmationEmailClickAction", function(){
		resendConfirmationEmail();

		return false;
	});

	/* Function to manage toggle block like FAQ questions */
	$(".toggle_block").on("click",".toggle_block_action", function(){
		$(this).siblings(".toggle_block_content").toggle();

		return false;
	});

	// hide law cookie bar on window scroll event
	// per ora lo commento
	/*$(document).on('scroll', window, function() {
		// lawCookieCompliance.removeMe();
	});*/
});

/**
 * 	Author: Entpy Software <developer at entpy dot com>
 * 	Version: 0.1.0
 * 	- wrapper for ajax call
 *  	- require jquery
 */
var loadDataWrapper = {

	__idPage : "",
	htmlLoaded : "",

	setIdPage : function(pageId){
		this.__idPage = pageId;
		return this.__idPage;
	},

	getIdPage : function(){
		return this.__idPage;
	},

	performAjaxCall : function(ajaxCallData){

		// setting ajax call data
		ajaxCallObj.setAjaxData(ajaxCallData);

		// performing ajax call
		ajaxCallObj.doAjaxCall();
	},
};

// wrapper to save page data
var saveDataWrapper = {

	__idPage: "",

	__setIdPage : function(pageId){
		this.__idPage = pageId;
		return this.__idPage;
	},

	getIdPage : function(){
		return this.__idPage;
	},

};

var ajaxCallObj = {

	__url : "",
	__type : "",
	__data : "",
	__cache : "",
	__success : "",
	__error : "",
	__async: "",
	__headers: "",

	// common wrappers params
	setAjaxDataEasy : function(){

		this.__type = "POST";
		this.__cache = false;
		this.__async = true;

		return true;
	},

	// setting ajax call params
	setAjaxData : function(dataToSet){

		// loading common wrappers params
		this.setAjaxDataEasy();

		if(dataToSet.url){
			this.__url = dataToSet.url;
		}

		if(dataToSet.type){
			this.__type = dataToSet.type;
		}

		if(dataToSet.data){
			this.__data = dataToSet.data;
		}

		if(dataToSet.cache){
			this.__cache = dataToSet.cache;
		}

		if(dataToSet.async === true || dataToSet.async === false){
			this.__async = dataToSet.async;
		}

		if(dataToSet.success){
			this.__success = dataToSet.success;
		}

		if(dataToSet.error){
			this.__error = dataToSet.error;
		}

		if(dataToSet.headers){
			this.__headers = dataToSet.headers;
		}

		return true;
	},

	// loading ajax call params
	getAjaxData : function(){

		return {
			"url" : this.__url,
			"type" : this.__type,
			"async" : this.__async,
			"data" : this.__data,
			"cache" : this.__cache,
			"success" : this.__success,
			"error" : this.__error,
			"headers" : this.__headers
		};
	},

	// performing ajax call with previously data
	doAjaxCall : function(){

		$.ajax({
			url: this.getAjaxData().url,
			type: this.getAjaxData().type,
			data: this.getAjaxData().data,
			async: this.getAjaxData().async,
			cache: this.getAjaxData().cache,
			success: this.getAjaxData().success,
			error: this.getAjaxData().error,
			headers: this.getAjaxData().headers
		});
	}
};

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
		imageTemplate = '<img style="width: 100%;" alt="Anteprima immagine" src="' + imageUrl + '">';
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

/* Function to retrieve info about user (name, points, ranking) */
function retrieveUserInfo(userId) {
	if (userId) {
		// save image id
		var retrieveUserInfoAjaxAction = customAjaxAction;
		// serialize form
		retrieveUserInfoAjaxAction.setAjaxCallParams("user_id=" + userId + "&");
		// setting action name
		retrieveUserInfoAjaxAction.setActionName("get_user_info");
		// success callback function
		var successCallback = function(jsonResponse) {
			// open bootstrap modal
			user_data = jsonResponse.user_info
			bootstrapModalsObect.showFavoriteUserModal(user_data.user_id, user_data.user_first_name, user_data.user_last_name, user_data.user_ranking, user_data.user_points, user_data.user_profile_image_url);
		};
		retrieveUserInfoAjaxAction.setAjaxSuccessCallbackFunction(successCallback);
		// perform ajax call to save a new profile image
		retrieveUserInfoAjaxAction.performAjaxAction();
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

/* Function to resend a confirmation email */
function resendConfirmationEmail() {
	var resendConfirmationEmailAjaxAction = customAjaxAction;
	// set async to false
	resendConfirmationEmailAjaxAction.setAsyncFlag(false);
	// setting action name
	resendConfirmationEmailAjaxAction.setActionName("resend_confirmation_email");
	// success callback function
	var successCallback = function(jsonResponse) {
	    // hide resend button and show alert
	    var htmlSuccessBlock = '<div class="alert alert-info">';
	    htmlSuccessBlock += '<p>Una nuova email di verifica ti è stata appena inviata, <b>clicca il link</b> al suo interno per confermare il tuo account.</p>';
	    htmlSuccessBlock += '</div>';
	    $(".resendEmailConfirmationContainerAction").html(htmlSuccessBlock);
	};
	resendConfirmationEmailAjaxAction.setAjaxSuccessCallbackFunction(successCallback);
	// perform ajax call to add favorite
	resendConfirmationEmailAjaxAction.performAjaxAction();

	return true;
}

/* Object to manage bootstrap modals */
var bootstrapModalsObect = {

	// popup message tags
	simple_message_tags : "popup_simple_message",
	success_message_tags : "popup_success",
	alert_message_tags : "popup_alert",
	error_message_tags : "popup_error",

	/* Function to write bootstrap modal inside body tag, only if not already exists */
	writeModalInsideBodyTag: function() {
		if (!$(".bootstrap_modal").length) {
			var bootstrapModal = '';
			bootstrapModal += '<div class="bootstrap_modal modal fade" tabindex="-1" role="dialog" aria-labelledby="myLargeModalLabel" aria-hidden="true">';
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
		// questo è un layer che non scompare se vengono aperte
		// modal in modo consecutivo, quindi lo nascondo io forzatamente
		$('.modal-backdrop').remove();
		$('body').attr("style", "padding-right: 0px;");
		$(".bootstrap_modal").removeData();
		$(".bootstrap_modal").remove();
		this.writeModalInsideBodyTag();

		return true;
	},

	/* Function to show bootstrap modal */
	showBootstrapModal: function() {
		$(".bootstrap_modal").modal('show');

		return true;
	},

	/* Function to hide bootstrap modal */
	/*hideBootstrapModal: function() {
		// close previously opened bootstrap modal
		$('.bootstrap_modal').modal('hide');
		// fix per aprire modal in modo consecutivo
		$('.modal-backdrop').hide();

		return true;
	},*/

	/* Function to show popup message with bootstrap modal */
	showPopupMessage : function(message, message_tags){
		if (message_tags == this.success_message_tags) {
			// show a success modal popup
			this.showSuccessModal(message);
		} else if (message_tags == this.alert_message_tags) {
			// show an alert modal popup
			this.showAlertModal(message);
		} else if (message_tags == this.error_message_tags) {
			// show an error modal popup
			this.showErrorModal(message);
		} else if (message_tags == this.simple_message_tags) {
			// show a simple message popup without style
			this.showMessageModal(message);
		}
	},

	/* custom bootstrap modal functions {{{ */
	/* Function to build and show image zoom bootstrap modal */
	showZoomImageModal: function(imageUrl) {
		if (imageUrl) {
			this.resetBootstrapModal();
			$(".bootstrap_modal").find('.modal-body').html(this.getImageHtmlBlock(imageUrl));
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
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
	showSuccessModal: function(message, popup_title) {
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
			if (popup_title) {
				$(".bootstrap_modal").find('.modal-title').html(popup_title);
			}
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show a message bootstrap modal */
	showMessageModal: function(message, popup_title) {
		if (message) {
			this.resetBootstrapModal();
			var messageBlockTemplate = '';
			messageBlockTemplate += '<div class="row">';
			messageBlockTemplate += '<div class="col-md-12 margin_top_30">';
			messageBlockTemplate += '<div class="alert">';
			messageBlockTemplate += message;
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '</div>';
			$(".bootstrap_modal").find('.modal-title').html("Ottimo");
			if (popup_title) {
				$(".bootstrap_modal").find('.modal-title').html(popup_title);
			}
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
			$(".bootstrap_modal").find('.modal-title').html("Gulp!");
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show an error bootstrap modal */
	showErrorModal: function(message) {
		if (message) {
			this.resetBootstrapModal();
			var messageBlockTemplate = '';
			messageBlockTemplate += '<div class="row">';
			messageBlockTemplate += '<div class="col-md-12 margin_top_30">';
			messageBlockTemplate += '<div class="alert alert-danger">';
			messageBlockTemplate += message;
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '</div>';
			$(".bootstrap_modal").find('.modal-title').html("Ops...");
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show favorite user bootstrap modal */
	showFavoriteUserModal: function(userId, userFirstName, userLastName, userRanking, userPoints, userProfileImageUrl) {
		this.resetBootstrapModal();
		var messageBlockTemplate = '';
		messageBlockTemplate += '<div class="row">';
		messageBlockTemplate += '<div class="col-md-8">';
		messageBlockTemplate += '<div class="favorite_popup_info_container">';
		if (userRanking) {
		    messageBlockTemplate += '<div><span class="favorite_popup_ranking_value">' + userRanking + '</span>a posizione</div>';
		}
		messageBlockTemplate += '<div class="favorite_popup_points_container"><span class="favorite_popup_points_value">' + userPoints + '</span> punti</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<div class="col-md-4">';
		messageBlockTemplate += '<img class="favorite_profile_image" alt="Immagine profilo" src="' + userProfileImageUrl + '"';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		$(".bootstrap_modal").find('.modal-title').html(userFirstName + ' ' + userLastName);
		$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button><a href="/passerella/dettaglio-utente/' + userId + '/" class="btn btn-success">Vai al profilo</a>');
		$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
		this.showBootstrapModal();

		return false;
	},

	/* Function to build and show welcome bootstrap modal */
	showWelcomeModal: function(userFirstName) {
		this.resetBootstrapModal();
		var messageBlockTemplate = '';
		messageBlockTemplate += '<div class="row">';
		messageBlockTemplate += '<div class="col-md-12">';
		messageBlockTemplate += '<p>';
		messageBlockTemplate += '<h4>Ciao ' + userFirstName + ',</h4>';
		messageBlockTemplate += 'questo è <b>Beauty and Pics</b>, il concorso più fico dell\'universo!<br />'
		messageBlockTemplate += 'Ecco qualche dritta per iniziare: <ol class="welcome_list"><li><b>Carica</b> un\'immagine profilo.</li><li><b>Carica</b> almeno 5/6 immagini del book.</li><li><b>Chiedi</b> ai tuoi amici e parenti di votarti.</li></ol>';
		messageBlockTemplate += 'Quindi aspetta i primi voti e tieni d\'occhio la classifica...pronta/o per diventare una star del web?';
		messageBlockTemplate += '</p>';
		messageBlockTemplate += '</div>';
		$(".bootstrap_modal").find('.modal-title').html("Benvenuta/o al concorso!");
		$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-success" data-dismiss="modal">Si, iniziamo!</button>');
		$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
		this.showBootstrapModal();

		return false;
	},

	/* Function to build and show system notify modal */
	showSystemNotifyModal: function(userFirstName, notifyToRead) {
		this.resetBootstrapModal();
		var messageBlockTemplate = '';
		messageBlockTemplate += '<div class="row">';
		messageBlockTemplate += '<div class="col-md-12">';
		messageBlockTemplate += '<p>';
		messageBlockTemplate += '<h4>' + userFirstName + ',</h4>';
		if (notifyToRead == 1) {
			messageBlockTemplate += 'hai <b>' + notifyToRead + '</b> nuova notifica ';
		} else {
			messageBlockTemplate += 'hai <b>' + notifyToRead + '</b> nuove notifiche ';
		}
		messageBlockTemplate += 'di <b>Beauty and Pics</b> da leggere.<br />'
		messageBlockTemplate += '</p>';
		messageBlockTemplate += '</div>';
		$(".bootstrap_modal").find('.modal-title').html("Sistema di notifiche");
		$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Ricorda in seguito</button><a href="/profilo/notifiche/" class="btn btn-success">Leggi ora</a>');
		$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
		this.showBootstrapModal();

		return false;
	},

	/* Function to build and show add image to photoboard bootstrap modal */
	showAddImageToPhotoboard: function(imageUrl, imageId) {
		if (imageUrl && imageId) {
			this.resetBootstrapModal();
			var messageBlockTemplate = '';
			messageBlockTemplate += '<div class="row">';
			messageBlockTemplate += '<div class="col-md-12">';
			messageBlockTemplate += '<p>';
			messageBlockTemplate += 'Stai per inserire la seguente immagine nella bacheca, confermi?'
			messageBlockTemplate += '</p>';
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '<div class="row"><div class="col-sm-4 col-sm-offset-4">' + this.getImageHtmlBlock(imageUrl) + '</div></div>';
			$(".bootstrap_modal").find('.modal-title').html("Conferma");
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Annulla</button><button type="button" class="btn btn-success addImageToPhotoboardAction" data-image-id="' + imageId + '" data-dismiss="modal">Conferma</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show send validation email bootstrap modal */
	showSendValidationEmail: function() {
		this.resetBootstrapModal();
		var messageBlockTemplate = '';
		messageBlockTemplate += '<div class="row">';
		messageBlockTemplate += '<div class="col-md-12 resendEmailConfirmationContainerAction">';
		messageBlockTemplate += '<p>';
		messageBlockTemplate += 'Una email di verifica ti è stata inviata in fase di registrazione, tuttavia puoi riceverne un\'altra premendo il pulsante <b>"Inviami email di verifica"</b>.<br />Infine, per confermare il tuo account, clicca sul link ricevuto via email.';
		messageBlockTemplate += '</p>';
		messageBlockTemplate += '<div class="row"><div class="col-xs-12 text-center"><button type="button" class="btn btn-success resendConfirmationEmailClickAction">Inviami email di verifica</button></div></div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		$(".bootstrap_modal").find('.modal-title').html("Conferma il tuo account");
		$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
		$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
		this.showBootstrapModal();

		return false;
	},

	/* Function to build and show vote user bootstrap modal */
	showVoteUserModal: function(userId, userFirstName, howItWorksImageUrl, selectionImageUrl, contestOpen, userRegistered, emailVerified) {
		this.resetBootstrapModal();
		var descriptionMessageBlock = "";
		var enableVoteButton = false;
		// debug var {{{
		/*contestOpen = true;
		userRegistered = true;
		emailVerified = true;*/
		// debug var }}}
		if (contestOpen && emailVerified && userRegistered) {
			descriptionMessageBlock = '<div class="alert alert-info"><p>Seleziona quale voto vuoi assegnare all\'utente. In base al voto scelto i punti verranno ripartiti su ogni metrica di valutazione.</p></div>';
			enableVoteButton = true;
		} else if (!contestOpen) {
			msg_text = 'Fino all\'apertura del concorso non sarà possibile votare';
			descriptionMessageBlock = '<div class="alert alert-warning"><p>Ci spiace, fino all\'apertura del concorso non sarà possibile votare.</p></div>';
		} else if (!userRegistered) {
			msg_text = 'Per votare devi prima registrarti';
			descriptionMessageBlock = '<div class="alert alert-warning"><p>Per votare devi prima registrarti, fallo ora per dare il tuo primo voto. <a class="alert-link" href="/registrazione-rapida/' + userId + '/">Registrazione rapida</a></p></div>';
		} else if (!emailVerified) {
			msg_text = 'Verifica il tuo indirizzo email per votare';
			descriptionMessageBlock = '<div class="alert alert-danger"><p>Attenzione per votare devi prima verificare il tuo indirizzo email.<br /><a class="alert-link openResendConfirmationModalClickAction" href="#">Clicca qui</a> per verificarlo ora.</p></div>';
		}

		var messageBlockTemplate = '';
		messageBlockTemplate += '<style>';
		messageBlockTemplate += '/* dropdown css fix for android browser z-index error (only for this modal) */';
		messageBlockTemplate += '.select_vote_type_container { position: relative; z-index: 1; }';
		messageBlockTemplate += '.vote_points_container { position: relative; z-index: -1; }';
		messageBlockTemplate += '.modal-content, .modal-footer { position: static; z-index: -1; }';
		messageBlockTemplate += '</style>';
		messageBlockTemplate += '<div class="row">';
		messageBlockTemplate += '<div class="col-md-12 small-no-padding">';
		messageBlockTemplate += descriptionMessageBlock;
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<div class="row select_vote_type_container">';
		messageBlockTemplate += '<div class="col-sm-6 col-xs-12 no-gutter">';
		messageBlockTemplate += '<!-- per visualizzazione desktop -->';
		messageBlockTemplate += '<div class="col-xs-12 vote_type_list no-gutter hidden-xs">';
		messageBlockTemplate += '<a class="voteItemAction voteItem_sguardo_ammaliante" data-vote-code="sguardo_ammaliante" href="#"><img alt="Selezione" src="' + selectionImageUrl + '">Sguardo ammaliante</a>';
		messageBlockTemplate += '<a class="voteItemAction voteItem_persona_solare" data-vote-code="persona_solare" href="#"><img alt="Selezione" src="' + selectionImageUrl + '">Persona solare</a>';
		messageBlockTemplate += '<a class="voteItemAction voteItem_troppo_stile" data-vote-code="troppo_stile" href="#"><img alt="Selezione" src="' + selectionImageUrl + '">Troppo stile</a>';
		messageBlockTemplate += '<a class="voteItemAction voteItem_che_classe" data-vote-code="che_classe" href="#"><img alt="Selezione" src="' + selectionImageUrl + '">Che classe</a>';
		messageBlockTemplate += '<a class="voteItemAction voteItem_impeccabile" data-vote-code="impeccabile" href="#"><img alt="Selezione" src="' + selectionImageUrl + '">Impeccabile</a>';
		messageBlockTemplate += '<a class="voteItemAction voteItem_notevole" data-vote-code="notevole" href="#"><img alt="Selezione" src="' + selectionImageUrl + '">Notevole</a>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<!-- per visualizzazione mobile -->';
		messageBlockTemplate += '<div class="col-xs-12 visible-xs-block vote_type_dropdown no-gutter margin_bottom_15 text-center">';
		messageBlockTemplate += '<div class="display_table centered_page">';
		messageBlockTemplate += '<div class="display_table_cell vertical_align_middle">';
		messageBlockTemplate += '<div class="btn-group">';
		messageBlockTemplate += '<a aria-expanded="false" href="#" class="btn btn-primary dropdown-toggle voteItemsDropdowAction" data-toggle="dropdown">';
		messageBlockTemplate += 'Seleziona voto <span class="caret"></span>';
		messageBlockTemplate += '</a>';
		messageBlockTemplate += '<ul class="dropdown-menu">';
		messageBlockTemplate += '<li><a class="voteItemAction voteItem_sguardo_ammaliante" data-vote-code="sguardo_ammaliante" href="#">Sguardo ammaliante</a>';
		messageBlockTemplate += '<li><a class="voteItemAction voteItem_persona_solare" data-vote-code="persona_solare" href="#">Persona solare</a>';
		messageBlockTemplate += '<li><a class="voteItemAction voteItem_troppo_stile" data-vote-code="troppo_stile" href="#">Troppo stile</a>';
		messageBlockTemplate += '<li><a class="voteItemAction voteItem_che_classe" data-vote-code="che_classe" href="#">Che classe</a>';
		messageBlockTemplate += '<li><a class="voteItemAction voteItem_impeccabile" data-vote-code="impeccabile" href="#">Impeccabile</a>';
		messageBlockTemplate += '<li><a class="voteItemAction voteItem_notevole" data-vote-code="notevole" href="#">Notevole</a>';
		messageBlockTemplate += '</ul>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<div class="display_table_cell vertical_align_middle">';
		messageBlockTemplate += '<a class="vote_how_it_works_link" href="/howto/le-votazioni/"><img class="vote_how_it_works_image" src="' + howItWorksImageUrl + '" alt="Come funziona?"></a>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<div class="vote_points_container col-sm-6 col-xs-12 no-gutter">';
		messageBlockTemplate += '<div class="hidden-xs vote_points_container_title col-xs-12">';
		messageBlockTemplate += '<div><h4>Ripartizione punti</h4></div>';
		messageBlockTemplate += '<div><a class="btn-link btn-xs no-gutter" href="/howto/le-votazioni/">Come funziona?</a></div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<div class="col-xs-6 col-sm-12">';
		messageBlockTemplate += '<!-- stats block -->';
		messageBlockTemplate += '<div class="smile_metric">';
		messageBlockTemplate += '<div class="stats_bar_label">Sorriso +<b class="metric_points">0</b></div>';
		messageBlockTemplate += '<div class="stats_bar">';
		messageBlockTemplate += '<div class="progress">';
		messageBlockTemplate += '<div class="progress-bar progress-bar-warning" role="progressbar" style="width: 0%"></div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<!-- stats block -->';
		messageBlockTemplate += '<div class="look_metric">';
		messageBlockTemplate += '<div class="stats_bar_label">Sguardo +<b class="metric_points">0</b></div>';
		messageBlockTemplate += '<div class="stats_bar">';
		messageBlockTemplate += '<div class="progress">';
		messageBlockTemplate += '<div class="progress-bar progress-bar-warning" role="progressbar" style="width: 0%"></div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<div class="col-xs-6 col-sm-12">';
		messageBlockTemplate += '<!-- stats block -->';
		messageBlockTemplate += '<div class="global_metric">';
		messageBlockTemplate += '<div class="stats_bar_label">Globale +<b class="metric_points">0</b></div>';
		messageBlockTemplate += '<div class="stats_bar">';
		messageBlockTemplate += '<div class="progress">';
		messageBlockTemplate += '<div class="progress-bar progress-bar-warning" role="progressbar" style="width: 0%"></div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '<!-- stats block -->';
		messageBlockTemplate += '<div class="style_metric">';
		messageBlockTemplate += '<div class="stats_bar_label">Stile +<b class="metric_points">0</b></div>';
		messageBlockTemplate += '<div class="stats_bar">';
		messageBlockTemplate += '<div class="progress">';
		messageBlockTemplate += '<div class="progress-bar progress-bar-warning" role="progressbar" style="width: 0%"></div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		messageBlockTemplate += '</div>';
		// modal title
		$(".bootstrap_modal").find('.modal-title').html("Dai il tuo voto a <b>" + userFirstName + "</b>");
		// modal footer
		if (enableVoteButton) {
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button><button type="button" class="btn btn-success confirmVoteButtonAction">Conferma il voto</button>');
		} else {
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button><button type="button" class="btn btn-default disabled-only-graphics alertVoteButtonAction" data-alert-text="' + msg_text + '">Conferma il voto</button>');
		}
		// modal content
		$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
		this.showBootstrapModal();

		return false;
	},

	/* Function to build and show a generic text modal with close button */
	showGenericTextModal: function(title, content) {
		if (title && content) {
			this.resetBootstrapModal();
			var messageBlockTemplate = '';
			messageBlockTemplate += '<div class="row">';
			messageBlockTemplate += '<div class="col-md-12">';
			messageBlockTemplate += '<p>' + content + '</p>';
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '</div>';
			$(".bootstrap_modal").find('.modal-title').html(title);
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show a publish survey modal */
	showPublishSurveyModal: function(content) {
		if (content) {
			this.resetBootstrapModal();
			var messageBlockTemplate = '';
			messageBlockTemplate += '<div class="row">';
			messageBlockTemplate += '<div class="col-md-12">';
			messageBlockTemplate += '<p>' + content + '</p>';
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '<div class="row"><div class="col-xs-12 text-center"><button type="button" class="btn btn-success publishSurveyClickAction">Pubblica adesso</button></div></div>';
			$(".bootstrap_modal").find('.modal-title').html("Pubblica la tua intervista");
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},

	/* Function to build and show photocontest info modal bootstrap modal */
	showPhotocontestInfoModal(photocontestCode, photocontestName, photocontestDescription, photocontestLikeLimit) {
		if (photocontestCode && photocontestName && photocontestDescription && photocontestLikeLimit) {
			this.resetBootstrapModal();
			var messageBlockTemplate = '';
			messageBlockTemplate += '<div class="row">';
			messageBlockTemplate += '<div class="col-md-4">';
			messageBlockTemplate += '<img alt="' + photocontestCode + '" src="/static/website/img/preferences_account_info.png">';
			messageBlockTemplate += '</div>';
			messageBlockTemplate += '<div class="col-md-8"><div>' + photocontestDescription + '</div><div>"Mi piace" richiesti: <b>' + photocontestLikeLimit + '</b></div></div>';
			messageBlockTemplate += '</div>';
			$(".bootstrap_modal").find('.modal-title').html(photocontestName);
			$(".bootstrap_modal").find('.modal-footer').html('<button type="button" class="btn btn-default" data-dismiss="modal">Annulla</button><button type="button" class="btn btn-success photocontestEnterClickAction" data-photocontest-code="' + photocontestCode + '" data-dismiss="modal">Partecipa</button>');
			$(".bootstrap_modal").find('.modal-body').html(messageBlockTemplate);
			this.showBootstrapModal();
		}

		return false;
	},
	/* custom bootstrap modal functions }}} */

	/* modal image block, with must be a size: eg. '100%' or '129px' or '12em' ecc... */
	getImageHtmlBlock: function(imageUrl, width) {
		var templateBlock = false;
		var imageWidth = "100%";
		if (width) {
			imageWidth = width;
		}
		if (imageUrl) {
			templateBlock = '<img style="width: ' + imageWidth + ';" alt="" src="' + imageUrl + '">';
		}

		return templateBlock;
	},

	deleteImageButtonHtmlBlock: function(imageId) {
		var templateBlock = false;
		if (imageId) {
			templateBlock = '<button type="button" class="btn btn-default" data-dismiss="modal">Chiudi</button><button type="button" data-image-id="' + imageId + '" class="btn btn-success deleteProfileImageClickAction">Cancella immagine</button>';
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
	__maxPoints : 8,
	__metrics_list : {
		'smile_metric' : 'smile_metric',
		'look_metric' : 'look_metric',
		'global_metric' : 'global_metric',
		'style_metric' : 'style_metric'
	},
	selectedVoteCode : false,
	votationIsValid : false,
	selectedVoteCodeClass : "selected_vote",
	voteUserId : false,
	ajaxCallUrl : "/ajax/",

	/* Function to calculate points percentage */
	getPointPercentage : function(points) {
		return pointPercentage = parseInt((points / this.__maxPoints) * 100);
	},

	/* Function called on vote_code selection */
	manageVoteCodeSelected : function(voteCode, userId) {
		if (voteCode && userId) {
			// setting points bar
			var singleVoteCodeData = this.getSingleVoteCodeData(voteCode);
			// show metric info on html
			this.showMetricInfo(this.__metrics_list["smile_metric"], singleVoteCodeData[this.__metrics_list["smile_metric"]])
			this.showMetricInfo(this.__metrics_list["look_metric"], singleVoteCodeData[this.__metrics_list["look_metric"]])
			this.showMetricInfo(this.__metrics_list["global_metric"], singleVoteCodeData[this.__metrics_list["global_metric"]])
			this.showMetricInfo(this.__metrics_list["style_metric"], singleVoteCodeData[this.__metrics_list["style_metric"]])

			// setto la classe selected_vote al vote_code cliccato
			this.setActiveVoteCodeSelected(voteCode);

			// setto la label corretta alla dropdown di bootstrap
			this.setDropdownText();

			// setto il vote code e abilito la votazione
			this.enableVotation(voteCode, userId);
		}

		return false;
	},

	/* setto la classe selected_vote al vote_code cliccato*/
	setActiveVoteCodeSelected : function(voteCode) {
		$(".voteItemAction").removeClass(this.selectedVoteCodeClass);
		$(".voteItem_" + voteCode).addClass(this.selectedVoteCodeClass);

		return true;
	},

	/* Function to enable votation */
	enableVotation : function(voteCode, userId) {
		this.selectedVoteCode = voteCode;
		this.voteUserId = userId;
		this.votationIsValid = true;

		return true;
	},

	/* Function to reset votation data */
	resetVotation : function() {
		this.selectedVoteCode = false;
		this.voteUserId = false;
		this.votationIsValid = false;

		return true;
	},

	/* Function to check if votation is enabled */
	getVotationIsEnabled : function() {
		var returnVar = false;
		if (this.selectedVoteCode && this.votationIsValid && this.voteUserId) {
			returnVar = true;
		}

		return returnVar;
	},

	/* Function to set dropdown text */
	setDropdownText : function() {
		// retrieve active element text
		var selectedText = $(".vote_type_dropdown").find("." + this.selectedVoteCodeClass).html();
		$(".vote_type_dropdown").find('.dropdown-toggle').html(selectedText+' <span class="caret"></span>');

		return true;
	},

	/* Function to show metric info about a vote_code on html */
	showMetricInfo : function(metricCode, metricPoints) {
		// setting point into label
		$("." + metricCode + " .metric_points").html(metricPoints);
		// setting bar width
		$("." + metricCode + " .progress-bar").css("width", this.getPointPercentage(metricPoints) + "%");

		return true;
	},

	/* Function to retrieve info about all vote_codes */
	getAllVoteCodesData : function() {
		return {
			'sguardo_ammaliante' : {
				'smile_metric' : '2',
				'look_metric' : '8',
				'global_metric' : '3',
				'style_metric' : '2'
			},
			'persona_solare' : {
				'smile_metric' : '8',
				'look_metric' : '2',
				'global_metric' : '2',
				'style_metric' : '3'
			},
			'troppo_stile' : {
				'smile_metric' : '3',
				'look_metric' : '2',
				'global_metric' : '3',
				'style_metric' : '7'
			},
			'che_classe' : {
				'smile_metric' : '2',
				'look_metric' : '2',
				'global_metric' : '8',
				'style_metric' : '3'
			},
			'impeccabile' : {
				'smile_metric' : '4',
				'look_metric' : '4',
				'global_metric' : '3',
				'style_metric' : '4'
			},
			'notevole' : {
				'smile_metric' : '4',
				'look_metric' : '4',
				'global_metric' : '4',
				'style_metric' : '3'
			}
		}
	},

	/* Function to retrieve info about a single vote_code */
	getSingleVoteCodeData : function(voteCode) {
		var return_var = false;
		if (voteCode) {
			var allVoteCodesData = this.getAllVoteCodesData();
			/*console.log("all vote_codes");
			console.log(allVoteCodesData[voteCode]);*/
			return_var = allVoteCodesData[voteCode];
		}

		return return_var;
	},

	/* Function to perform an action after confirm vote button click */
	confirmVoteButtonClickAction : function() {
		if (!this.getVotationIsEnabled()) {
			alert("Devi prima selezionare un voto.");
		} else {
			if (confirm("Confermi il voto? Potrai votare nuovamente questo partecipante tra 7 giorni.")) {
				this.performVoteAction();
			}
		}

		return false;
	},

	/* Function to perform a vote action */
	performVoteAction : function() {
		if (this.getVotationIsEnabled()) {
			// reading csrfmiddlewaretoken from cookie
			var csrftoken = readCsrftokenFromCookie();
			var ajaxCallData = {
				url : this.ajaxCallUrl,
				data : "user_id=" + this.voteUserId + "&vote_code=" + this.selectedVoteCode + "&ajax_action=perform_voting",
				async : false,
				headers: { "X-CSRFToken": csrftoken },
				success : function(jsonResponse) {
					// functions to manage JSON response
					console.log("==========risultato chiamata==========");
					console.log(jsonResponse);
					if (jsonResponse.success) {
						voteUserObject.performVoteSuccessCallback(jsonResponse.message)
					} else if (jsonResponse.error) {
						voteUserObject.performVoteErrorCallback(jsonResponse.message)
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

	/* Function to close bootstrap vote modal */
	closeVoteBootstrapModal : function() {
		$('.bootstrap_modal').modal('hide');
	},

	/* Success callback function  */
	performVoteSuccessCallback : function(message) {
		// show success message
                alert(message);
                $(".successVoteMessageAction").removeClass("hide");
		// hide default info text
                $(".voteInfoMessageAction").addClass("hide");
                // hide vote form
                $(".voteFormContainerAction").addClass("hide");
		// closing bootstrap modal
		this.closeVoteBootstrapModal();

		return true;
	},

	/* Error callback function  */
	performVoteErrorCallback : function(message) {
		// show error message
                alert(message);

		return true;
	}
};

/* Object to retrieve a filtered list of elements (user, photo book, favorites, notify, photoboard) */
var elementsListObject = {
	__elementsListFilters : {
		"user_id" : null, // required in "favorites" and "book" elementsListType
		"elements_list_type" : null, // catwalker, favorite, photobook, notify, photoboard
		"start_limit" : 0, // element retrieving start limit
		"show_limit" : 1, // element retrieving stop limit
		"elements_per_call" : 1, // number of element retrieved per call
		"filter_name" : null, // main filter (Es. latest_registered, classification, ecc...)
	}, // list of AND filters */
	ajaxCallUrl : "/ajax/", // the ajax call url
	bootstrapBlockSize : null, // the bootstrap block size for display
	blocksContainerClassName : ".image_grid_container", // the block container class inside html page
	tableBlocksContainerClassName : ".table_body_block_container", // the block container class inside html page
	actionButtonClassName : ".loadMoreElementsAction", // load more button class name

	/* Function to reset all filters */
	__resetFilters : function() {
		this.__elementsListFilters["user_id"] = null;
		this.__elementsListFilters["elements_list_type"] = null;
		this.__elementsListFilters["start_limit"] = 0;
		this.__elementsListFilters["show_limit"] = 1;
		this.__elementsListFilters["elements_per_call"] = 1;
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

	/* Function to set element show limit */
	setElementsPerCall : function(elementsPerCall) {
		if (elementsPerCall) {
			// retrieve previously added filters
			var existing_filters = this.getElementsListFilters();
			existing_filters["elements_per_call"] = elementsPerCall;
			existing_filters["show_limit"] = elementsPerCall;
			// setting new filters object
			this.setElementsListFilters(existing_filters);
		}

		return true;
	},

	/* Function to set element start limit */
	/*setStartLimit : function(startLimit) {
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
	/*setShowLimit : function(showLimit) {
		if (showLimit) {
			// retrieve previously added filters
			var existing_filters = this.getElementsListFilters();
			existing_filters["show_limit"] = showLimit;
			// setting new filters object
			this.setElementsListFilters(existing_filters);
		}

		return true;
	},*/

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
		// hide "load more" button
		elementsListObject.hideActionButton();
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

				// show or hide "load more" button
				if (jsonResponse.show_load_button) {
				    elementsListObject.showActionButton();
				} else {
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
				} else if (jsonResponse.elements_list_type == "last_upload") {
					// build and write block into html
					elementsListObject.writeHtmlBlock(elementsListObject.manageFavoriteList(jsonResponse.elements_list));
				} else if (jsonResponse.elements_list_type == "notify") {
					// build and write table blocks into html
					elementsListObject.writeTableHtmlBlock(elementsListObject.manageTableElementsList(jsonResponse.elements_list));
				} else if (jsonResponse.elements_list_type == "photoboard") {
					// build and write block into html
					elementsListObject.writeHtmlBlock(elementsListObject.managePhotoboardList(jsonResponse.elements_list));
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
		$(this.actionButtonClassName).addClass("display_none");
	},

	showActionButton : function() {
	/* Function to show action button */
		$(this.actionButtonClassName).removeClass("display_none");
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
			items += elementsListObject.getSingleHtmlBlock(blockUrl, blockThumbnailImageUrl, false, false, false);
		});
		// return jQuery object
		return $(items);
	},

	manageFavoriteList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(index, singleElement) {
			blockUrl = "#";
			blockThumbnailImageUrl = singleElement.thumbnail_image_url;
			items += elementsListObject.getSingleHtmlBlock(blockUrl, blockThumbnailImageUrl, false, "zoom-image", singleElement.user_id);
		});

		// return jQuery object
		return $(items);
	},

	manageTableElementsList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(index, singleElement) {
			items += elementsListObject.getSingleHtmlNotifyTableBlock(singleElement.notify_id, singleElement.title, singleElement.creation_date, singleElement.already_read);
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

	managePhotoboardList : function(elementsList) {
	/* Function to retrieve an html blocks list, this must be appended to html page */
		var items = "";
		$.each(elementsList, function(index, singleElement) {
			blockUrl = "/passerella/bacheca/" + singleElement.user_id;
			blockThumbnailImageUrl = singleElement.thumbnail_image_url;
			items += elementsListObject.getSingleHtmlBlock(blockUrl, blockThumbnailImageUrl);
		});

		// return jQuery object
		return $(items);
	},

	getSingleHtmlBlock : function(blockUrl, blockThumbnailImageUrl, blockImageUrl, imgTagClass, imgId, imgAlt) {

		returnVar = "";
		if (!imgTagClass) {
			imgTagClass = "";
		}

		if (!imgId) {
			imgId = "";
		}

		if (!imgAlt) {
			imgAlt = "Immagine del book";
		}

		if (blockUrl && blockThumbnailImageUrl) {
			// setting bootstrap block size
			if (!this.bootstrapBlockSize) {
				this.bootstrapBlockSize = true;
			}

			// retrieve bootstrap block size
			var blockSize = this.getBlockSize();
			// build html block with link and image
			var returnVar = '<div class="col-lg-' + blockSize["lg_size"] + ' col-md-' + blockSize["md_size"] + ' col-xs-' + blockSize["xs_size"] + ' col-sm-' + blockSize["sm_size"] + ' thumb imgBlockContainer_' + imgId + '"><a href="' + blockUrl + '" class="thumbnail"><img alt="' + imgAlt + '" src="' + blockThumbnailImageUrl + '" data-fullimage-url="' + blockImageUrl + '" data-image-id="' + imgId + '" class="img-responsive ' + imgTagClass + '"></a></div>'
		}

		return returnVar;
	},

	getSingleHtmlNotifyTableBlock : function(notifyId, notifyTitle, notifyCreationDate, notifyAlreadyRead) {
	/* Function to build notify table html blocks */

		returnVar = "";

		if (notifyTitle && notifyId) {
			// action to read notify
			var actionLink = '/profilo/notifiche/' + notifyId;
			if (notifyAlreadyRead) {
				returnVar = '<tr><td><a class="table_action_link " href="' + actionLink + '">' + notifyTitle + '</a></td><td class="display_only_big">' + notifyCreationDate + '</td><td class="text-center"><a class="alert-link" href="' + actionLink + '"><span class="label label-default">letta</span></a></td></tr>';
			} else {
				returnVar = '<tr><td><a class="table_action_link" href="' + actionLink + '">' + notifyTitle + '</a></td><td class="display_only_big">' + notifyCreationDate + '</td><td class="text-center"><a class="alert-link" href="' + actionLink + '"><span class="label label-success">da leggere</span></a></td></tr>';
			}
		}

		return returnVar;
	},

	getBlockSize : function() {
	/* Function to retrieve bootstrap block size */
		// setting bootstrap block size
		if (!this.bootstrapBlockSize) {
			this.bootstrapBlockSize = true;
		}
		var blockSize = Array();
		blockSize["lg_size"] = (this.bootstrapBlockSize["lg_size"] ? this.bootstrapBlockSize["lg_size"] : "15");
		blockSize["md_size"] = (this.bootstrapBlockSize["md_size"] ? this.bootstrapBlockSize["md_size"] : "3");
		blockSize["sm_size"] = (this.bootstrapBlockSize["sm_size"] ? this.bootstrapBlockSize["sm_size"] : "3");
		blockSize["xs_size"] = (this.bootstrapBlockSize["xs_size"] ? this.bootstrapBlockSize["xs_size"] : "6");

		return blockSize;
	},

	writeHtmlBlock : function(htmlBlocksList) {
	/* function to append blocks into html container */
		// console.log(htmlBlocksList);
		// alert("blocchi 'scritti' con successo" + this.blocksContainerClassName);
		$(this.blocksContainerClassName).append(htmlBlocksList);
	},

	writeTableHtmlBlock : function(htmlBlocksList) {
	/* function to append blocks into html container */
		// console.log(htmlBlocksList);
		// alert("blocchi 'scritti' con successo" + this.blocksContainerClassName);
		$(this.tableBlocksContainerClassName).append(htmlBlocksList);
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
		if (!$.isEmptyObject(jsonResponse) && !$.isEmptyObject(jsonResponse["form_data"])) {
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

/* Object to manage law cookie div */
// Creare's 'Implied Consent' EU Cookie Law Banner v:2.4
// Conceived by Robert Kent, James Bavington & Tom Foyster
var lawCookieCompliance = {
	dropCookie : true, // false disables the Cookie, allowing you to style the banner
	cookieDuration : 60, // Number of days before the cookie expires, and the banner reappears
	cookieName : 'complianceCookie', // Name of our cookie
	cookieValue : 'on', // Value of cookie

	createDiv : function() {
		var bodytag = document.getElementsByTagName('body')[0];
		var div = document.createElement('div');
		div.setAttribute('id', 'cookie-law');
		div.innerHTML = '<p>Su questo sito utilizziamo i cookie. Per saperne di più <a href="/cookie-policy" rel="nofollow" title="Cookies Policy">clicca qui</a>. Continuando la navigazione acconsenti al loro utilizzo.&nbsp;&nbsp;<a class="close-cookie-banner" href="javascript:void(0);" onclick="lawCookieCompliance.removeMe();"><span>X</span></a></p>';
		// bodytag.appendChild(div); // Adds the Cookie Law Banner just before the closing </body> tag
		// or
		bodytag.insertBefore(div, bodytag.firstChild); // Adds the Cookie Law Banner just after the opening <body> tag
		document.getElementsByTagName('body')[0].className += ' cookiebanner'; //Adds a class tothe <body> tag when the banner is visible
		this.createCookie(lawCookieCompliance.cookieName, lawCookieCompliance.cookieValue, lawCookieCompliance.cookieDuration); // Create the cookie
	},

	createCookie : function(name, value, days) {
		if (days) {
			var date = new Date();
			date.setTime(date.getTime()+(days*24*60*60*1000)); 
			var expires = "; expires="+date.toGMTString(); 
		} else var expires = "";
		if(lawCookieCompliance.dropCookie) { 
			document.cookie = name+"="+value+expires+"; path=/"; 
		}
	},

	checkCookie : function(name) {
		var nameEQ = name + "=";
		var ca = document.cookie.split(';');
		for(var i=0;i < ca.length;i++) {
			var c = ca[i];
			while (c.charAt(0)==' ') c = c.substring(1,c.length);
			if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
		}
		return null;
	},

	eraseCookie : function(name) {
		this.createCookie(name,"",-1);
	},

	removeMe : function() {
		var element = document.getElementById('cookie-law');
		if(element) element.parentNode.removeChild(element);
	},

	createDivOnLoad : function() {
		if(this.checkCookie(lawCookieCompliance.cookieName) != lawCookieCompliance.cookieValue){
			this.createDiv(); 
		}
	},
};

// Facebook JavaScript SDK
window.fbAsyncInit = function() {
	FB.init({
		appId : '932261456835509',
		xfbml : true,
		version : 'v2.4'
	});
};
