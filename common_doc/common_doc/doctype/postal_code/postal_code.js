// Copyright (c) 2022, John and contributors
// For license information, please see license.txt

frappe.ui.form.on('Postal Code', {
	// refresh: function(frm) {

	// }
	onload_post_render(frm) {
		if (!frm.doc.location && frm.doc.latitude && frm.doc.longitude) {
			frm.fields_dict.location.map.setView([frm.doc.latitude, frm.doc.longitude], 13);
		}
		else {
			frm.doc.latitude = frm.fields_dict.location.map.getCenter()['lat'];
			frm.doc.longitude = frm.fields_dict.location.map.getCenter()['lng'];
		}
	},
});
