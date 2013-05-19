// Calcultae items total, render total and run optional callback
// function renderTotal(items, callback) {
// 	var amount = _.reduce(items, function(total, item) { return total + parseFloat(item.total) }, 0).toFixed(2);

// 	$('.hondler-cart .total .amount').html(amount);
// 	callback(amount);

// 	return amount;
// }

// Fill up items container
// function renderItems(items) {
// 	var cartTpl = Handlebars.compile($('#cart').html());

// 	HONDLER.items = items;

// 	$('.hondler-cart .items')
// 		.toggleClass('hidden', !(items || []).length)
// 		.html(cartTpl({'STATIC_URL': STATIC_URL, 'items': items}));

// 	return items;
// }

// $('.hondler-product .actions .to-cart').on('click', function() {
// 	var $actions = $(this).closest('.actions');
	
// 	loading($actions);
	
// 	$.getJSON(CART_URLS('add', cleanId($(this).closest('.product'))), function(data, status) {
// 		if(status != 'success')
// 			return false;
		
// 		// Calculate cart total and render it
// 		renderTotal(data);
		
// 		// Render current cart items
// 		renderItems(data);
// 	}).complete(function() { loading($actions) });

// 	return false;
// });

// $('.hondler-cart .items .actions .remove').on('click', function() {
// 	loading($(this).closest('td'));
	
// 	$.getJSON(CART_URLS('remove', cleanId($(this).closest('tr'))), function(data, status) {
// 		if(status != 'success')
// 			return false;
			
// 		renderTotal(data);
// 		renderItems(data);
		
// 		// Redurect to main page when everything removed from cart on checkout page
// 		if(window.location.pathname == CART_URLS('checkout') && !data.length)
// 			window.location = '/';
// 	});

// 	return false;
// });

// $('.hondler-cart .update').on('click', function() {
// 	// Walk through cart items and update
// 	_.each(HONDLER.items, function(I) {
// 		var quantity = parseInt($(this).closest('.hondler-cart').find('.items tr#p' + I.id + ' .quantity input').val());

// 		_.extend(I, { 
// 			'quantity': quantity,
// 			'total': (quantity * parseFloat(I.price)).toFixed(2)
// 		});
// 	}, this);

// 	// Save updated cart items in DB
// 	$.post(CART_URLS('update'), {
// 		'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
// 		'items': JSON.stringify(HONDLER.items)
// 	}, function(data, status) {
// 		if(status != 'success')
// 			return false;
// 	});

// 	renderItems(HONDLER.items);
// 	renderTotal(HONDLER.items, shipping());
		
// 	return false;
// });

var Hondler = function(options) {
	this.cartTpl = options.cartTpl;
	this.items   = [];
	this.$items  = options.items;
	this.$total  = options.total;

	this.urls = {
		add: options.addURL,
		items: options.itemsURL,
		remove: options.removeURL,
		update: options.updateURL
	};
}

Hondler.prototype = {
	add: function(id) {
		var thiz = this;

		return $.getJSON(this.urls.add(id), function(data, status) {
			if(status != 'success')
				return false;
			
			// Calculate cart total and render it
			thiz.renderTotal(data);
			
			// Render current cart items
			thiz.renderItems(data);
		})
	},

	remove: function(id) {
		var thiz = this;

		return $.getJSON(this.urls.remove(id), function(data, status) {
			if(status != 'success')
				return false;
				
			thiz.renderTotal(data);
			thiz.renderItems(data);
			
			// Redurect to main page when everything removed from cart on checkout page
			if(window.location.pathname == CART_URLS('checkout') && !data.length)
				window.location = '/';
		});
	},

	// Fill up items container
	renderItems: function(items, callback) {
		this.items = items;

		this.$items.html(this.cartTpl({'items': items}));

		if(callback)
			callback(items);

		return items;
	},

	// Calcultae items total, render total and run optional callback
	renderTotal: function(items, callback) {
		var amount = _.reduce(items, function(total, item) { return total + parseFloat(item.total) }, 0).toFixed(2);

		this.$total.html(amount);

		if(callback)
			callback(amount);

		return amount;
	},

	updateCart: function(getQuantity) {
		// Walk through cart items and update
		_.each(this.items, function(I) {
			var quantity = getQuantity(id); //parseInt($(this).closest('.hondler-cart').find('.items tr#p' + I.id + ' .quantity input').val());

			_.extend(I, {
				quantity: quantity,
				total: (quantity * parseFloat(I.price)).toFixed(2)
			});
		}, this);

		// Save updated cart items in DB
		$.post(this.urls.update(), {
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
			items: JSON.stringify(this.items)
		}, function(data, status) {
			if(status != 'success')
				return false;
		});

		// Do not wait for request to be completed
		renderItems(HONDLER.items);
		renderTotal(HONDLER.items, shipping());
			
		return false;
	},

	// Update cart items on page
	updateItems: function(totalCb, itemsCb) {
		var thiz = this;

		$.getJSON(this.urls.items(), function(data, status) {
			if(status != 'success')
				return false;

			thiz.renderTotal(data, totalCb);
			thiz.renderItems(data, itemsCb);
		});
	}
};