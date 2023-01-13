frappe.pages['programing-page'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Demo Page',
		single_column: true
	});
	page.set_title('My Page')
	page.set_indicator('Done','green')
	let $btn = page.set_primary_action('New',() => frappe.msgprint("Clecked New"),'octicon octicon-plus') 
	let $btnOne = page.set_secondary_action('Refresh',()=> frappe.msgprint('Clicked Refresh'),"fa fa-refresh")
	page.add_menu_item('Send Email',()=> frappe.msgprint("Clicked Send Email"))
	page.add_action_item('Delete', () => frappe.msgprint("Clicked Delte"))
	let field = page.add_field({
		lable : 'Status',
		fieldtype : 'Select',
		fieldname : 'status',
		options : [
			'Open',
			'Closed',
			'Cancelled'
		],
		change() {
			frappe.msgprint(field.get_value());
		}
	}
	)
	// $(frappe.render_template("programing_page",{})).appendTo(page.body);
	$(frappe.render_template("programing_page",{
		data:"Hi Frappe"
	})).appendTo(page.body);
}