/**
 * 	Author: Ivan Torchio <i.torchio at entpy dot com>
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
 *
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

	getGenericDataViaAjaxCall : function(ajaxCallData){

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
