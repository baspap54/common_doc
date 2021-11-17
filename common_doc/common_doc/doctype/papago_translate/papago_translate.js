// Copyright (c) 2021, John and contributors
// For license information, please see license.txt

frappe.ui.form.on('Papago Translate', {
	refresh: function(frm) {
	frm.add_custom_button(__('Papago API'),function(){
            //frappe.msgprint(frm.doc.date);

            let source = frm.selected_doc.source;
            let source_text = frm.selected_doc.source_text;
            let target = frm.selected_doc.target;
            let target_text = frm.selected_doc.target_text;

            var me = this;

            frappe.call({
				method: "common_doc.common_doc.doctype.papago_translate.api.get_translate", //dotted path to server method
				args: {
					'source':source,
					'source_text':source_text,
					'target':target

				},

				callback: function(r) {

					console.log(r)
					if(r.message) {
						// code snippet

						cur_frm.set_value('source',r.message.source);
						cur_frm.set_value('source_text',r.message.source_text);
						cur_frm.set_value('target',r.message.target);

						cur_frm.set_value('target_text',r.message.target_text);



						return;
						//cur_frm.set_value('exchange_rate',r.message.exchange_rate);
						//cur_frm.exchange_rate = r.message.exchange_rate;

						}
				}
			})
        }, __("Translate")    );

	}
});