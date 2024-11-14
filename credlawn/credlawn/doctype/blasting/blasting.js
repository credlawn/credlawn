frappe.ui.form.on('Blasting', {
    onload: function(frm) {
        $(frm.wrapper).find('.help-box.small.text-muted').hide();
        
        if (!frm.is_new()) {
            const fields = ['lead_status', 'campaign_date', 'cr_date', 'lead_type', 'campaign_type', 'customer_name', 'mobile_no', 'city', 'data_source'];
            fields.forEach(field => {
                frm.set_df_property(field, 'read_only', frm.doc[field] ? true : false);
            });
        }
    }
});
