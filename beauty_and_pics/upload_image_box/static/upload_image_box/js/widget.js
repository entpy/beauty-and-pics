/* uploaderImageBox widget to manage different modal type */
var uploaderImageBox = {
	// current opened modal window instance
	modalWindow: false,
	// modal window settings, like buttons, content, titles, ecc...
	modalWindowSettings: {
		"base_modal": {"hidden_form": {"action": "/upload_image/upload/"}, "body": {"html": function() { return uploaderImageBox.__buildBaseModalBodyHtml("base_modal"); }}, "header": {"title": "Load an image"}, "footer": {"cancel": {"exists": true, "label": "Cancel"}}},
		"upload_modal": {"hidden_form": {"action": "/upload_image/upload/"}, "body": {"html": function() { return uploaderImageBox.__buildUploadModalBodyHtml("upload_modal"); }}, "header": {"title": "Image upload..."}, "footer": {"cancel": {"exists": true, "label": "Cancel"}}},
		"crop_modal": {"hidden_form": {"action": "/upload_image/crop/"}, "body": {"html": function() { return uploaderImageBox.__buildCropModalBodyHtml("crop_modal"); }, "crop_image_url": false, "crop_image_id": false}, "header": {"title": "Crop your image"}, "footer": {"cancel": {"exists": true, "label": "Cancel"}, "change_image": {"exists": true, "label": "Change image"}}},
		"preview_modal": {"hidden_form": {"action": "/upload_image/upload/"}, "body": {"html": function() { return uploaderImageBox.__buildPreviewModalBodyHtml("preview_modal"); }}, "header": {"title": "Image preview"}, "footer": {"cancel": {"exists": true, "label": "Cancel"}, "change_image": {"exists": true, "label": "Change image"}}},
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
		hiddenForm += '<form class="upload_image_box_form" name="upload_image_box_form" enctype="multipart/form-data" action="" method="POST" style="display: none;">';
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
	__buildBaseModalBodyHtml: function(modalType) {
		var modalTemplate = '';
		modalTemplate += '<div class="row">';
		modalTemplate += '<div class="col-md-12 text-center">';
		modalTemplate += '<button type="button" class="btn btn-success fileSelectClickAction">Select image</button>';
		modalTemplate += '</div>';
		modalTemplate += '</div>';

		// setting hidden form action url
		$(".upload_image_box_form").attr("action", this.modalWindowSettings[modalType]["hidden_form"]["action"])

		return modalTemplate;
	},
	__buildUploadModalBodyHtml: function() {},

	__buildCropModalBodyHtml: function(modalType) {
		var modalTemplate = '';
		modalTemplate += '<div class="row">';
		modalTemplate += '<div class="col-md-12 text-center">';
		modalTemplate += '<div class="cropper_container">';
		modalTemplate += '<img style="max-width: 450px; max-height: 450px;" class="crop_image_tag" data-file-id="' + this.modalWindowSettings[modalType]["body"]["crop_image_id"] + '" src="' + this.modalWindowSettings[modalType]["body"]["crop_image_url"] + '">';
		modalTemplate += '</div><br />';
		modalTemplate += '<button type="button" class="btn btn-success cropImageClickAction">Ritaglia</button>';
		modalTemplate += '</div>';
		modalTemplate += '</div>';

		return modalTemplate;
	},

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

	/* Function to init crop library */
	cropperInit: function() {
		// crop library -> http://fengyuanchen.github.io/cropper/
		$('.crop_image_tag').cropper({
			aspectRatio: 1 / 1,
			autoCropArea: 0.9,
			minCropBoxWidth: 200,
			minCropBoxHeight: 200,
			checkImageOrigin: false,
			touchDragZoom: false,
			strict: false,
			guides: true,
			highlight: true,
			dragCrop: true,
			movable: true,
			zoomable: false,
			rotatable: false,
			resizable: false
		});
	},

	/* Function to retrieve an option value */
	getOptionValue: function(optionName) {
		var return_var = false;
		if (optionName) {
			return_var = $(".uploader_image_box_options").data(optionName);
		}

		return return_var;
	},
};

/* Object to manage image crop */
var fileManager = {
	/* function to send a file via AJAX == submitting hidden form */
	sendFile: function() {
		var options = {
			//beforeSubmit:  showRequest,  // TODO: show "upload_modal" with loader
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
	loadUploadedImage: function(responseText, statusText, xhr, $form) { 
		// console.log('status: ' + statusText + '\n\nresponseText: \n');
		console.log(responseText);
		// load uploaded image via AJAX inside "crop_modal" or "preview_modal" window
		uploaderImageBox.modalWindowSettings["crop_modal"]["body"]["crop_image_url"] = responseText.file_url
		uploaderImageBox.modalWindowSettings["crop_modal"]["body"]["crop_image_id"] = responseText.file_id
		uploaderImageBox.openModalWindow("crop_modal");
		// crop library init
		uploaderImageBox.cropperInit();
	},

	/* Function to perform an ajax call */
	performAjaxCall: function(ajaxCallData) {
		var request = $.ajax({
			headers: { "X-CSRFToken": uploaderImageBox.getCookie('csrftoken') },
			url: ajaxCallData["url"],
			method: "POST",
			data: ajaxCallData["data"], // { id : menuId },
			dataType: "json"
		});

		request.done(function(msg) {
			// ajax call success
			// console.log(msg)
		});

		request.fail(function(jqXHR, textStatus) {
			// ajax call error
			console.log("Request failed: " + textStatus);
		});
	},

	/* Function to save cropped image */
	saveCroppedImage: function(ajaxCallData) {
		this.performAjaxCall(ajaxCallData);
	},
};

// Function to open modal window
$(document).on("click", ".uploaderButtonClickAction", function(){
	// open modal window
	uploaderImageBox.openModalWindow("base_modal");

	return false;
});

// Function to select an upload file
$(document).on("click", ".fileSelectClickAction", function(){
	// open file chooser
	$(".select_image_input").click();

	return false;
});

// Function to save upload cropped area
$(document).on("click", ".cropImageClickAction", function(){
	var cropData = $(".crop_image_tag").cropper('getData')
	var fileId = $(".crop_image_tag").data('fileId');
	var ajaxCallData = {
		"url": uploaderImageBox.modalWindowSettings["crop_modal"]["hidden_form"]["action"],
		"data": {
			"file_id": fileId,
			"x": cropData["x"],
			"y": cropData["y"],
			"width": cropData["width"],
			"height": cropData["height"],
			"rotate": cropData["rotate"],
			"custom_crop_dir_name": uploaderImageBox.getOptionValue("customUploadDirName"),
		}
	};

	// ajax call with image id and crop data
	fileManager.saveCroppedImage(ajaxCallData);

	// TODO: close modal window

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
