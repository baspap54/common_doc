// Copyright (c) 2021, John and contributors
// For license information, please see license.txt

frappe.ui.form.on('Port Code', {
	// refresh: function(frm) {
	onload_post_render(frm) {
		if (!frm.doc.port_code && frm.doc.latitude && frm.doc.longitude) {
			frm.fields_dict.location.map.setView([frm.doc.latitude, frm.doc.longitude], 13);
		}
		else {
			frm.doc.latitude = frm.fields_dict.location.map.getCenter()['lat'];
			frm.doc.longitude = frm.fields_dict.location.map.getCenter()['lng'];
		}
	},

	// }
});
