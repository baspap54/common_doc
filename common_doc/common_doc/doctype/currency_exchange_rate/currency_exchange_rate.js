// Copyright (c) 2021, John and contributors
// For license information, please see license.txt


frappe.ui.form.on('Currency Exchange Rate', {
	refresh: function(frm) {
	    frm.add_custom_button(__('Single KRW Currency KEB'),function(){
            //frappe.msgprint(frm.doc.date);
            let exchange_date = frm.selected_doc.date;
            let from_currency = frm.selected_doc.from_currency;
            let to_currency = frm.selected_doc.to_currency;
            let currency_exchange_rate_type = frm.selected_doc.currency_exchange_rate_type;
            var me = this;

            if(to_currency == "KRW"){

            frappe.call({
				method: "common_doc.common_doc.doctype.currency_exchange_rate.api.get_exchange_rate", //dotted path to server method
				args: {
					'exchange_date':exchange_date,
					'from_currency':from_currency,
					'to_currency':to_currency,
					'currency_exchange_rate_type' : currency_exchange_rate_type
				},

				callback: function(r) {

					console.log(r)
					//cur_frm.exchange_rate = r.message.exchange_rate;
					if(r.message) {
						// code snippet
						//frappe.msgprint();
						//frappe.msgprint({
						//	title: __('Exchange rate created'),
						//	message: __('Check exchange rate')+r.message.exchange_rate,
						//	indicator: 'orange'
						//});
						//frm.selected_doc.exchange_rate = r.message.exchange_rate;
						cur_frm.set_value('rate',r.message.rate);
						cur_frm.set_value('date',r.message.date);
						cur_frm.set_value('usd_rate',r.message.usd_rate);
						cur_frm.set_value('scale',r.message.scale);

						return;
						//cur_frm.set_value('exchange_rate',r.message.exchange_rate);
						//cur_frm.exchange_rate = r.message.exchange_rate;

						}
				}
			})
			}
        }, __("Get exchange rate")    );
	    frm.add_custom_button(__('ALL KRW Currency KEB'),function(){
            //frappe.msgprint(frm.doc.date);
            let exchange_date = frm.selected_doc.date;
            let from_currency = frm.selected_doc.from_currency;
            let to_currency = frm.selected_doc.to_currency;
            let currency_exchange_rate_type = frm.selected_doc.currency_exchange_rate_type;

            if(to_currency == "KRW"){
				frappe.call({
					method: "common_doc.common_doc.doctype.currency_exchange_rate.api.get_exchange_rate_all", //dotted path to server method
					args: {
						'exchange_date':exchange_date,
						'from_currency':from_currency,
						'to_currency':to_currency,
						'currency_exchange_rate_type' : currency_exchange_rate_type
					},

					callback: function(r) {

						console.log(r)
						// code snippet
						frappe.msgprint({
							title: __('Exchange rate created'),
							message: __('KEB exchange rates are created'),
							indicator: 'orange'

						});



					}
				})
			}
        }, __("Get exchange rate")    );



     }
});