/* uploaderImageBox widget to manage different modal type */
var uploaderImageBox = {
	// current opened modal window instance
	modalWindow: false,
	// modal window settings, like buttons, content, titles, ecc...
	modalWindowSettings: {
		"base_modal": {"hidden_form": {"url": "/upload_image/upload/"}, "body": {"html": function() { return uploaderImageBox.__buildBaseModalBodyHtml(); }}, "header": {"title": "Load an image"}, "footer": {"cancel": {"exists": true, "label": "Cancel"}}},
		"upload_modal": {"hidden_form": {"url": "/upload_image/upload/"}, "body": {"html": function() { return uploaderImageBox.__buildUploadModalBodyHtml(); }}, "header": {"title": "Image upload..."}, "footer": {"cancel": {"exists": true, "label": "Cancel"}}},
		"crop_modal": {"hidden_form": {"url": "/upload_image/upload/"}, "body": {"html": function() { return uploaderImageBox.__buildCropModalBodyHtml(); }}, "header": {"title": "Crop your image"}, "footer": {"cancel": {"exists": true, "label": "Cancel"}, "change_image": {"exists": true, "label": "Change image"}}},
		"preview_modal": {"hidden_form": {"url": "/upload_image/upload/"}, "body": {"html": function() { return uploaderImageBox.__buildPreviewModalBodyHtml(); }}, "header": {"title": "Image preview"}, "footer": {"cancel": {"exists": true, "label": "Cancel"}, "change_image": {"exists": true, "label": "Change image"}}},
	},

	/* Function to read options and write modal html inside "modal_container" container */
	init: function() {
		console.log("upload_image_box widget init...");
		this.__writeModalTemplateInsideHtml();
		this.__writeHiddenForm();
	},

	/* Function to retrieve modal window html code */
	__writeModalTemplateInsideHtml: function() {
		$(".modal_container").html(this.__getModalTemplateHtml());
	},

	/* function to write an hidden form */
	__writeHiddenForm: function() {
		var hiddenForm = '';
		hiddenForm += '<form class="upload_image_box_form" name="upload_image_box_form" action="" method="POST" style="display: none;">';
		hiddenForm += '<input type="hidden" value="' + this.getCookie('csrftoken') + '" name="csrfmiddlewaretoken">';
		hiddenForm += '<input class="select_image_input" type="file" name="image" />';
		hiddenForm += '</form>';
		$(".modal_container").parents("form").after(hiddenForm);
	},

	/* Function to write modal window scheleton */
	__getModalTemplateHtml: function() {
		var modalTemplate = '';
		modalTemplate += '<div id="upload_image_box_modal" class="modal fade bs-example-modal-md" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">';
		modalTemplate += '<div class="modal-dialog modal-md">';
		modalTemplate += '<div class="modal-content">';
		modalTemplate += '<div class="modal-header"></div>';
		modalTemplate += '<div class="modal-body">';
		modalTemplate += '</div>';
		modalTemplate += '<div class="modal-footer"></div>';
		modalTemplate += '</div>';
		modalTemplate += '</div>';
		modalTemplate += '</div>';

		return modalTemplate;
	},

	/* Functions to build modal windows body {{{ */
	__buildBaseModalBodyHtml: function() {

		var modalTemplate = '';
		modalTemplate += '<div class="row">';
		modalTemplate += '<div class="col-md-12 text-center">';
		modalTemplate += '<button type="button" class="btn btn-success fileSelectClickAction">Select image</button>';
		modalTemplate += '</div>';
		modalTemplate += '</div>';

		// TODO: setting hidden form url

		return modalTemplate;
	},
	__buildUploadModalBodyHtml: function() {},
	__buildCropModalBodyHtml: function() {},
	__buildPreviewModalBodyHtml: function() {},
	/* Functions to build modal windows body }}} */

	/* Function to write modal window header */
	__getModalTemplateHeaderHtml: function() {
		var modalTemplate = '';
		modalTemplate += '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
		modalTemplate += '<h4 class="modal-title" id="gridSystemModalLabel">Modal title</h4>';

		return modalTemplate;
	},

	/* Function to write modal window footer */
	__getModalTemplateFooterHtml: function(modalType) {
		var modalTemplate = '';
		if (this.modalWindowSettings[modalType]["footer"].hasOwnProperty("cancel")) {
			modalTemplate += '<button type="button" class="btn btn-default" data-dismiss="modal">' + this.modalWindowSettings[modalType]["footer"]["cancel"]["label"] + '</button>';
		}
		if (this.modalWindowSettings[modalType]["footer"].hasOwnProperty("change_image")) {
			modalTemplate += '<button type="button" class="btn btn-primary fileSelectClickAction">' + this.modalWindowSettings[modalType]["footer"]["change_image"]["label"] + '</button>';
		}

		return modalTemplate;
	},

	/*
	Modal windows type:
	===================
		base_modal: modal opened after upload click button
		upload_modal: modal opened after all images upload, userful to see a percentage about upload process
		crop_modal: modal opened after first image upload, userful to crop an image
		preview_modal: modal opened after first image upload, userful to see a preview of uploaded image
	*/
	/* Function to write a modal window and apply all settings (buttons, title, content, ecc...) */
	buildModalWindow: function(modalType) {
		// load modal window html elements
		this.modalWindow.find('.modal-header').html(this.__getModalTemplateHeaderHtml());
		this.modalWindow.find('.modal-footer').html(this.__getModalTemplateFooterHtml(modalType));
		// change loaded elements with bootstrap modal interface
		this.modalWindow.find('.modal-title').text(this.modalWindowSettings[modalType]["header"]["title"]);
		this.modalWindow.find('.modal-body').html(this.modalWindowSettings[modalType]["body"]["html"]);
	},

	/* Function to open a modal window by type */
	openModalWindow: function(modalType) {
		this.modalWindow = $('#upload_image_box_modal').modal();
		this.buildModalWindow(modalType);

		return true;
	},

	/* Function to read a cookie */
	getCookie: function(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) == (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	},
};

var fileManager = {

	/* function to send a file via AJAX == submitting hidden form */
	sendFile: function() {
		var options = {
			//beforeSubmit:  showRequest,  // pre-submit callback 
			success:       this.loadUploadedImage  // post-submit callback 

			// other available options: 
			//url:       url         // override for form's 'action' attribute 
			//type:      type        // 'get' or 'post', override for form's 'method' attribute 
			//dataType:  null        // 'xml', 'script', or 'json' (expected server response type) 
			//clearForm: true        // clear all form fields after successful submit 
			//resetForm: true        // reset the form after successful submit 

			// $.ajax options can be used here too, for example: 
			//timeout:   3000 
		}; 

		// prepare hidden form to submit
		$(".upload_image_box_form").ajaxForm(options); 
		// submit hidden form
		$(".upload_image_box_form").submit();
		// reset hidden form
		$(".upload_image_box_form").resetForm();
	},

	/* Function to load uploaded image inside modal window body */
	loadUploadedImage: function(responseText, statusText, xhr, $form)  { 
		alert('status: ' + statusText + '\n\nresponseText: \n' + responseText + '\n\nThe output div should have already been updated with the responseText.');
	}
}

// Function to open modal window
$(document).on("click", ".uploaderButtonClickAction", function(){
	uploaderImageBox.openModalWindow("base_modal");

	return false;
});

// function to select an upload file
$(document).on("click", ".fileSelectClickAction", function(){
	console.log("Select a file to upload");
	// open file chooser
	$(".select_image_input").click();

	return false;
});

// function to send a file on "onChange" event
$(document).on("change", ".select_image_input", function(){
	// submit hidden form
	fileManager.sendFile();
	// TODO
	// show upload modal to show upload status bar
	// show uploaded image into crop view

	return false;
});
