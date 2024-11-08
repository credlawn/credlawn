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
        "* * * * *": [  # This runs every minute
            "credlawn.scripts.create_short_url.create_route_redirects"
            # "credlawn.scripts.send_new_lead.send_lead",  # This is commented out
        ],
        "0 0 * * *": [  # This runs every day at midnight
            "credlawn.scripts.update_employee_age_n_tenure.scheduled_employee_update"
        ],
        "0 * * * *": [  # This runs every hour
            "credlawn.scripts.email_processing.enqueue_email_processing"
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

