from subprocess import call
from subprocess import check_output
from glob import glob
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

def get_domains():
    for e in glob("/servers/*"):
        yield os.path.basename(e)

def get_live_domain_and_exparation_date():
    certificates = glob("/etc/letsencrypt/live/*/cert.pem")
    for e in certificates:
        domain = os.path.basename(os.path.dirname(e))
        out = check_output(["./get_exparation_date.sh", e])
        exparation_date = datetime.strptime(out,"notAfter=%b  %d %H:%M:%S %Y GMT\n")
        yield domain, exparation_date


sched = BlockingScheduler(timezone="UTC")

domains = list(get_domains())

now = datetime.utcnow()

def get_updater(domain):
    def result():
        print "renuing for domain:", domain
        call(["./update_cert.sh",domain])
    return result

for dom, exp in get_live_domain_and_exparation_date():
    if dom in domains:
        domains.remove(dom)
        date_to_renew= exp - timedelta(days=30)
        if date_to_renew - now > timedelta(days=1):
            print "scheduling for domain:", dom, "\trenew due:", date_to_renew
            sched.add_job(get_updater(dom),'interval', days=60, next_run_time=date_to_renew)
        else:
            to_run = get_updater(dom)
            sched.add_job(to_run,'interval', days=60)
            to_run()

sched.start()
