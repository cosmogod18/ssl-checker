#!/usr/bin/python3.8
import ssl
import socket
from datetime import date
import datetime
from mailer import Mailer


msg = Mailer()

TODAY = date.today()
NOW = datetime.datetime.now()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class SslChecker():
        def __init__(self, *args, **kwargs):
                """
                Application Config. All parameters are changeble.

                """
                self.RECEIVE_EMAIL = True                                               # Change to False if you dont wanna get emails.
                self.subject = f"{TODAY} SSL expire soon. less then in 10 days"         # Email subject.
                self.FROM = "linux-admin@penki.lt"                                      # Email sender.
                self.filename = '/root/2021/django-ssl-checker/domain_list.txt'         # Text file with domain list to check for SSL expiration.
                self.domains = []                                                       # List of domains that need SSL upgrade.
                self.days = 10                                                          # Check if SSL expires less than in 10 days.



        def calculate_dates(self, exp, now):
                delta = exp - now
                days = str(delta).split('days')
                return int(days[0])

        def check_expire_date(self):
                with open(self.filename, 'r') as list_domains:
                        for domain in list_domains:
                                try:
                                        striped_domain = domain.strip('\n')
                                        ssl_date_frmt = r'%b %d %H:%M:%S %Y %Z'
                                        context = ssl.create_default_context()
                                        conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=striped_domain)
                                        conn.settimeout(1)
                                        conn.connect((striped_domain, 443))
                                        ssl_info = conn.getpeercert()
                                        expire_date = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_frmt)

                                        if self.calculate_dates(expire_date, NOW) >= self.days:
                                                print(bcolors.BOLD + '{:<50}'.format(f"{striped_domain}") + bcolors.ENDC + bcolors.OKGREEN + f'LEFT {self.calculate_dates(expire_date, NOW)}'+ bcolors.ENDC)
                                        else:
                                                print(bcolors.BOLD + '{:<50}'.format(f"{striped_domain}") + bcolors.ENDC + bcolors.WARNING + f'LEFT {self.calculate_dates(expire_date, NOW)}'+ bcolors.ENDC)
                                                self.domains.append(striped_domain)
                                except Exception as error:
                                        print(bcolors.BOLD + '{:<50}'.format(f"{striped_domain}") + bcolors.ENDC + bcolors.FAIL + f'ERROR: {error}'+ bcolors.ENDC)

                converted = '\n'.join(map(str, self.domains))
                if self.RECEIVE_EMAIL == True:
                        if len(converted) != 0:
                                msg.sendMessage(self.subject, self.FROM, converted)
                        else:
                                pass
                else:
                        pass

if __name__ == "__main__":
        app = SslChecker()
        app.check_expire_date()
