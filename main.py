from app.logs.logger import write_logs
from app.ui.dashboard import Dashboard

try:
    dashboard = Dashboard()
    dashboard.run()
    
except Exception as error:
    write_logs(error)