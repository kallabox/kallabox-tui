import sys
import um.user_app as user_man
import sam.sa_app as super_man


if len(sys.argv) >= 2 and sys.argv[1].lower() == "admin":
    # Run as admin mode
    super_man.service_mode()


else:
    # Run as user mode
    user_man.user_mode()
