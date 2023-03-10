frappe.listview_settings["Currency Exchange Rate"] = {
    onload: function (listview) {
		listview.page.add_menu_item(__("Create KEB Exchange Rate"), function() {
            const dialog = new frappe.ui.Dialog({
    			title: __('Exchange Date'),
    			fields: [
    			    {fieldtype: 'Date', label: __('Exchange Date'), fieldname: 'exchange_date', reqd: 1}
    			    
    			    ],
			primary_action: function({ exchange_date }) {
				frappe.call({
                    method: "common_doc.common_doc.doctype.currency_exchange_rate.api.get_exchange_rate_all", //dotted path to server method
					args: {
						'exchange_date':exchange_date
					},
					freeze: true,
					callback: function() {
						dialog.hide();
						frappe.msgprint({
							message: __('Successfully Created'),
							alert: true
						});
					},
					error: function() {
						dialog.hide();
						frappe.msgprint({
							message: __('Creattion Failed. Please try again.'),
							title: __('KE Exchange Rate Entry Failed'),
							indicator: 'red'
						});
					}
				});
			},
			primary_action_label: __('Create KEB')
    		});
    		dialog.show();
		})
    }
}