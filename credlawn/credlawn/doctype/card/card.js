// Copyright (c) 2024, Credlawn India and contributors
// For license information, please see license.txt

frappe.ui.form.on('check_pan_card', 'refresh', function(frm) {
  // Get PAN card value from the form
  var pan_card = frm.doc.pan_card;

  // Check if PAN card is empty
  if (!pan_card) {
    return;  // Exit if no PAN card entered
  }

  // Function to perform AJAX call for PAN card check
  function checkPANCard(pan_card) {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: '/api/method/Credlawn.credlawn.doctype.card.check_pan.pan_status',  // Adjusted URL for custom app
        type: 'POST',
        data: { pan_card: pan_card },
        dataType: 'json',
        success: function(data) {
          resolve(data.message);
        },
        error: function(error) {
          reject(error);  // Handle AJAX errors
        }
      });
    });
  }

  // Call the checkPANCard function and display the message
  checkPANCard(pan_card)
    .then(message => {
      frappe.msgprint(message);  // Display message in the form
    })
    .catch(error => {
      console.error("Error checking PAN card:", error);
      frappe.msgprint("An error occurred. Please try again.", validate=True);
    });
});

