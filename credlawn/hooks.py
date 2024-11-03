app_name = "credlawn"
app_title = "Credlawn"
app_publisher = "Credlawn India Private Limited"
app_description = "CRM"
app_email = "info@credlawn.com"
app_license = "mit"





app_include_css = [
    "/assets/credlawn/css/credlawn.css" 
]


scheduler_events = {
    "cron": {
        "* * * * *": [
            # "credlawn.scripts.send_new_lead.send_lead",
        ],
        "0 0 * * *": [  # This runs every day at midnight
            "credlawn.scripts.update_employee_age_n_tenure.scheduled_employee_update"
        ],
        "0 * * * *": [  # This runs every hour
            "credlawn.scripts.get_new_leads_from_url_shortener.fetch_and_process_urls",
            "credlawn.scripts.update_clicks_from_url.fetch_visitor_record",
            "credlawn.scripts.email_processing.enqueue_email_processing"
        ],
        "*/5 * * * *": [  # This runs every 5 minutes
            "credlawn.scripts.create_short_url.run_post_request"
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

