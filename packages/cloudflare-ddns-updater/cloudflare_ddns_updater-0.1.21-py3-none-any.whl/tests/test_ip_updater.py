import shutil
import sys
from crontab import CronTab

cron_comment = "Cron job for Cloudflare DDNS ip-updater"


def check_ip_updater_exists():
    # Find the full path of 'ip-updater' command
    ip_updater_path = shutil.which('ip-updater')
    ip_updater_path = "ip_updater"
    if not ip_updater_path:
        print("ip-updater command not found. Try a fresh installation.")
        sys.exit(1)
    return ip_updater_path


def delete_cron_job():
    # Access the user's crontab
    cron = CronTab(user=True)  # Use 'user=False' for root's crontab
    # Remove the found jobs
    for job in cron:
        if job.comment == cron_comment:
            print(f"Removing cron job: {job}")
            cron.remove(job)
            cron.write()
            return
    print("No Cron Jobs to remove")
    return


def new_cronjob():
    cron = CronTab(user=True)
    ip_updater_path = check_ip_updater_exists()
    job = cron.new(command=f"{ip_updater_path} >> /var/log/ip_update.log 2>&1", comment=cron_comment)
    job.minute.every('3')
    cron.write()
    return


def toggle_cron_job(toggle):
    cron = CronTab(user=True)
    for job in cron:
        if job.comment == cron_comment:
            job.enable(toggle)
            cron.write()
    return


# Example usage
delete_cron_job()
# new_cronjob()
# toggle_cron_job(True)
