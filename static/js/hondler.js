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

	getTotal: function(items) {
		return (_.reduce(items, function(total, item) {
			return total + parseFloat(item.total)
		}, 0) + parseFloat(this.shippingCost || 0)).toFixed(2);
	},

	itemsCount: function() { return this.items.length },

	remove: function(id) {
		var thiz = this;

		return $.getJSON(this.urls.remove(id), function(data, status) {
			if(status != 'success')
				return false;
				
			thiz.renderTotal(data);
			thiz.renderItems(data);
		});
	},

	// Fill up items container
	renderItems: function(items, callback) {
		this.items = items;
		
		// Do not render empty items
		this.$items.html(this.cartTpl({
			items: _.filter(this.items, function(I) { return Boolean(parseInt(I.quantity)) })
		}));

		if(callback)
			callback(items);

		return items;
	},

	// Calcultae items total, render total and run optional callback
	renderTotal: function(items, callback) {
		var amount = this.getTotal(items);

		this.$total.html(amount);

		if(callback)
			callback(amount);

		return amount;
	},

	setShipping: function(cost) {
		this.shippingCost = cost;
		this.renderTotal(this.items);
	},

	update: function(getQuantityFunc) {
		// Walk through cart items and update
		_.each(this.items, function(I) {
			var quantity = getQuantityFunc(I.id);

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
		this.renderItems(this.items);
		this.renderTotal(this.items);
			
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