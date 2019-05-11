#!/usr/bin/python3

from subprocess import run
from subprocess import check_output
from glob import glob
import os
from datetime import datetime, timedelta
from shutil import copyfile
from apscheduler.schedulers.blocking import BlockingScheduler

def get_domains():
    for e in glob("/httpser/servers/*"):
        yield os.path.basename(e)

def get_live_domains:
    certificates = glob("/etc/letsencrypt/live/*/cert.pem")
    for e in certificates:
        domain = os.path.basename(os.path.dirname(e))
        yield domain

def get_cert(domain):
    print("getting cert for domain %s" % domain)
    out = run([
    "certbot",
    "certonly",
    "--non-interactive",
    "--agree-tos",
    "-m",
    "example@mail.com",
    "--webroot",
    "-w",
    "/var/www",
    "-d",
    domain
    ],stdout=subprocess.DEVNULL)
    if out.returncode != 0:
        print("renewing of domain %s failed with code %d" % (domain, out.returncode))

def update(domain):
    print("renewing cert for domain %s" % domain)
    run([
    "certbot",
    "certonly",
    "--non-interactive",
    "--agree-tos",
    "-m",
    "example@mail.com",
    "--webroot",
    "-w", "/var/www",
    "-d",
    domain
    ],stdout=subprocess.DEVNULL)

def get_updater(domain):
    return lambda : update(domain)

def get_exparation_date(domain):
    certificate = "/etc/letsencrypt/live/%s/cert.pem" % domain
    out = check_output([
    "openssl",
    "x509",
    "-enddate",
    "-noout",
    "-in",
    certificate])
    return datetime.strptime(out,"notAfter=%b  %d %H:%M:%S %Y GMT\n")

def reload():
    run(["nginx", "-s", "reload"], stdout=subprocess.DEVNULL)

def start():
    run(["nginx"], stdout=subprocess.DEVNULL)

reloading = os.path.isfile("/var/run/nginx.pid"):

sched = BlockingScheduler(timezone="UTC")
domains = list(get_domains())
live_domains = list(get_live_domains())

if not reloading:
    start()

for dom in domains:
    if dom in live_domains:
        domains.remove(dom)
        exp = get_exparation_date(dom)
        date_to_renew = exp - timedelta(days=30)
        copyfile(os.path.join("/httpser/servers",dom,"http."+dom+".conf"),"/httpser/actives")
        copyfile(os.path.join("/httpser/servers",dom,"https."+dom+".conf"),"/httpser/actives")

        reload()
        if date_to_renew - datetime.utcnow() > timedelta(days=1): # no need to update now

            print("scheduling renewing for domain %s with renew date %s" % (dom, date_to_renew))
            sched.add_job(get_updater(dom),'interval', days=60, next_run_time=date_to_renew)
        else: #need to update now
            print("scheduling renewing for domain %s with renew date %s" % (dom, date_to_renew + timedelta(days=60)))
            sched.add_job(get_updater(dom),'interval', days=60)
            update(dom)
    else:
        copyfile(os.path.join("/httpser/servers",dom,"http."+dom+".conf"),"/actives")
        reload()
        print("scheduling renewing for domain %s with renew date %s" % (dom, date_to_renew + timedelta(days=60)))
        sched.add_job(get_updater(dom),'interval', days=60)
        get_cert(dom)
        copyfile(os.path.join("/servers",dom,"https."+dom+".conf"),"/actives")
        reload()
        print("%s is online" % dom)

for e in glob("/httpser/actives/*"):
    first_dot = e.find('.')
    saved_file_domain = e[first_dot + 1:-len(".conf")]
    if saved_file_domain not in domains:
        os.remove(e)

sched.start()
