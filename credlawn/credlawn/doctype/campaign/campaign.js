frappe.ui.form.on('Campaign', {
    refresh: function(frm) {
        if (!frm.is_local && frm.doc.campaign_type === 'SMS' && frm.doc.campaign_status !== 'Success') {
            frm.add_custom_button(__('Run Campaign'), function() {
                
                frappe.call({
                    method: "credlawn.scripts.send_sms_campaign.send_sms",
                    args: { "campaign_name": frm.doc.name },
                    
                    callback: function(response) {
                        if (!response.exc) {
                            frm.set_value('campaign_status', 'Success');
                            frappe.msgprint(__('Campaign Started in Background'));
                       
                        } else {
                            frm.set_value('campaign_status', 'Failed');
                            frappe.msgprint(__('An error occurred while starting the campaign.'));
                        }
                        frm.save();
                    }
                });
            });
        }
    }
});
