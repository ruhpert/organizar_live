var Todo_Model = (function(_this, $) {
	var todos = null;
	var menu = null;
	var ANIMATION_TIME = 500;

	_this.init = function() {
		console.log("~~~ TODO MODEL INIZIALIZED ~~~")
		todos = $("#todos");
		menu = todos.find(".menu");
		
		_this.handle_show_hide();
		_this.handle_hover();
	};

	_this.handle_hover = function() {
		var todo_list = todos.find(".todo");

		todo_list.mouseenter(function() {
			var todo = $(this);
			var hidden_data = todo.find(".hidden-data");
			hidden_data.show();
		}).mouseleave(function() {
			var todo = $(this);
			var hidden_data = todo.find(".hidden-data");
			hidden_data.hide();
		});
	};
	
	_this.handle_show_hide = function() {
		var triggerButton = menu.find(".show-hide-todos");

		todos.animate({
			"right" : -150 + "px",
		}, ANIMATION_TIME);
		
		triggerButton.click(function() {
			var clickedButton = $(this);

			if (clickedButton.hasClass("out")) {
				clickedButton.removeClass("out");
				clickedButton.html("&lt;");

				todos.animate({
					"right" : -150 + "px",
				}, ANIMATION_TIME);
			}
			else {
				clickedButton.addClass("out");
				clickedButton.html("&gt;");

				todos.animate({
					"right" : 0 + "px",
				}, ANIMATION_TIME);
			}
		})
	};

	return _this;

}({},jQuery));