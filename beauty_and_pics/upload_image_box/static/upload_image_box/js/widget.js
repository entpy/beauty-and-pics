/* uploaderImageBox widget to manage different modal type */
var uploaderImageBox = {
	modalWindow: false,
	init: function() {
		// reading options and write modal html inside "modal_container" container
		console.log("upload_image_box widget init...");
		this.writeModalTemplateInsideHtml();
	},

	/* Function to write modal window scheleton */
	__getModalTemplateHtml: function() {
		var modalTemplate = '';
		modalTemplate += '<div id="upload_image_box_modal" class="modal fade bs-example-modal-md" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel" aria-hidden="true">';
		modalTemplate += '<div class="modal-dialog modal-md">';
		modalTemplate += '<div class="modal-content">';
		modalTemplate += '<div class="modal-header"></div>';
		modalTemplate += '<div class="modal-body">';
		modalTemplate += 'Contenuto della finestra modale';
		modalTemplate += '</div>';
		modalTemplate += '<div class="modal-footer"></div>';
		modalTemplate += '</div>';
		modalTemplate += '</div>';
		modalTemplate += '</div>';

		return modalTemplate;
	},

	/* Function to write modal window header */
	__getModalTemplateHeaderHtml: function() {
		var modalTemplate = '';
		modalTemplate += '<button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>';
		modalTemplate += '<h4 class="modal-title" id="gridSystemModalLabel">Modal title</h4>';

		return modalTemplate;
	},

	/* Function to write modal window footer */
	__getModalTemplateFooterHtml: function() {
		var modalTemplate = '';
		modalTemplate += '<button type="button" class="btn btn-default" data-dismiss="modal">Close</button>';
		modalTemplate += '<button type="button" class="btn btn-primary">Save changes</button>';

		return modalTemplate;
	},

	/* Function to write modal window inside container */
	writeModalTemplateInsideHtml: function() {
		$(".modal_container").html(this.__getModalTemplateHtml());
	},

	/*
	Modal windows type:
	===================
		base_modal: modal opened after upload click button
		upload_modal: modal opened after all images upload, userful to see a percentage about upload process
		crop_modal: modal opened after first image upload, userful to crop an image
		preview_modal: modal opened after first image upload, userful to see a preview of uploaded image
	*/
	/* Function to write base modal window */
	baseModalWindow: function() {
		this.modalWindow.find('.modal-header').html(this.__getModalTemplateHeaderHtml());
		this.modalWindow.find('.modal-footer').html(this.__getModalTemplateFooterHtml());
		this.modalWindow.find('.modal-title').text("Carica un'immagine")
	},

	/* Function to open a modal window by type */
	openModalWindow: function(modalType) {
		this.modalWindow = $('#upload_image_box_modal').modal();
		if (modalType == "base_modal") {
			this.baseModalWindow();
		}

		return true;
	},
};
$(document).on("click", ".uploaderButtonClickAction", function(){
	uploaderImageBox.openModalWindow("base_modal");

	return false;
});
