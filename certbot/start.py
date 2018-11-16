from subprocess import call
from subprocess import check_output
from glob import glob
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler


running_file = "/var/www/certbot.running"
open(running_file, 'a').close()
print "is file: ", os.path.isfile(running_file)
print "created file"

def get_domains():
    for e in glob("/servers/*/domains.txt"):
        with open(e) as f:
            lines = f.readlines()
            for l in lines:
                yield l

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
            sched.add_job(get_updater(dom),'interval', days=60, next_run_time=datetime.now())


for dom in domains:
    sched.add_job(get_updater(dom),'interval', days=60, next_run_time=datetime.now())

os.remove(running_file)
sched.start()
