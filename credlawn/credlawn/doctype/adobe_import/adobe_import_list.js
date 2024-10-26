frappe.listview_settings['Adobe Import'] = {
    onload: function(listview) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper, .layout-main-section').css('margin-left', '0');
        $('.page-container').addClass('no-sidebar');

        listview.page.add_inner_button(__('Update Status'), function() {
            frappe.call({
                method: 'credlawn.scripts.find_duplicate_in_adobe_import.update_file_type',
                callback: function(response) {
                    frappe.msgprint(response.message || __('No message returned.'));
                },
                error: function(err) {
                    frappe.msgprint(__('Error: ') + err.message);
                }
            });
        });
    }
};
