frappe.listview_settings['Bank Links'] = {
    onload: function(listview) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper, .layout-main-section').css('margin-left', '0');
        $('.page-container').addClass('no-sidebar');
    }
};
