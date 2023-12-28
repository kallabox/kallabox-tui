import application_manager as app_man
import super_admin_application_manager as super_man
import sys

# total arguments
if len(sys.argv) >= 2 and sys.argv[1].lower() == "admin":
    # Run as admin mode
    super_man.service_mode()


else:
    # Run as user mode
    app_man.user_mode()
