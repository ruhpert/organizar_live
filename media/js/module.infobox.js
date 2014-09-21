/******************************************
 * 
 * 
 * MODULE Infobox
 * 
 * 
 * *****************************************/
var Infobox = (function($, _this) {

	var infobox = null;
	var infoboxContent = null;
	var infoboxBg = null;

	$(document).ready(function() {
		infobox = $(".status-info-wrapper");
		infoboxContent = infobox.find(".status-info");
		infoboxClose = infobox.find(".close");

		infoboxClose.click(function() {
			_this.hide();
		});
	});

	_this.showMessage = function(theMessage) {
		infobox.fadeIn(200);
		infoboxContent.html(theMessage);
	};
	
	_this.hide = function() {
		infobox.fadeOut(200);
	};
	
	return _this;
}(jQuery, {}));
