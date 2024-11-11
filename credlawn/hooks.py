app_name = "credlawn"
app_title = "Credlawn"
app_publisher = "Credlawn India Private Limited"
app_description = "CRM"
app_email = "info@credlawn.com"
app_license = "mit"





app_include_css = [
    "/assets/credlawn/css/credlawn.css" 
]

webhooks = [
    {
        "method": "POST",
        "url": "/api/method/credlawn.webhook.sms_delivery_report.get_sms_delivery_report"
    }
]



scheduler_events = {
    "cron": {
        "0 0 * * *": [  # This runs every day at midnight
            "credlawn.scripts.update_employee_age_n_tenure.scheduled_employee_update"
        ],
        "0 * * * *": [  # This runs every hour
            "credlawn.scripts.email_processing.enqueue_email_processing",
            "credlawn.scripts.clean_redirect_link.delete_redirect_link"
        ]
        
    }
}












# scheduler_events = {
# 	"all": [
# 		"credlawn.tasks.all"
# 	],
# 	"daily": [
# 		"credlawn.tasks.daily"
# 	],
# 	"hourly": [
# 		"credlawn.tasks.hourly"
# 	],
# 	"weekly": [
# 		"credlawn.tasks.weekly"
# 	],
# 	"monthly": [
# 		"credlawn.tasks.monthly"
# 	],
# }

