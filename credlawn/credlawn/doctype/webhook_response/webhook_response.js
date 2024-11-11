frappe.ui.form.on('Webhook Response', {
    onload: function(frm) {
        $(frm.wrapper).find('.help-box.small.text-muted').hide();
    }
});
