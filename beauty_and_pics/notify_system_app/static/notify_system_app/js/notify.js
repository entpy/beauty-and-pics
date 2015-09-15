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
	// count unread notify
	count_unread_notify();
});

/* Function to count unread notify */
function count_unread_notify() {
	// save image id
	var ajaxObject = customAjaxAction;
	// setting action name
	ajaxObject.setActionName("count_unread_notify");
	// success callback function
	var successCallback = function(jsonResponse) {
		// open bootstrap modal
		unread_notify_total = jsonResponse.unread_notify_total
		user_first_name = jsonResponse.user_first_name
		if (unread_notify_total) {
			bootstrapModalsObect.showSystemNotifyModal(user_first_name, unread_notify_total);
		}
	};
	ajaxObject.setAjaxSuccessCallbackFunction(successCallback);
	// perform ajax call to save a new profile image
	ajaxObject.performAjaxAction();
}
