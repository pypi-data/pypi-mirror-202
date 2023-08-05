#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This package implements local hostname resolver tool with scapy (using netbios and LLMNR query).
#    Copyright (C) 2021, 2023  Maurice Lambert

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
###################

"""
This package implements local hostname resolver tool with scapy (using netbios and LLMNR query).
"""

__version__ = "0.0.3"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = (
    "This package implements local hostname resolver tool with scapy (using netbios and LLMNR query)."
)
license = "GPL-3.0 License"
__url__ = "https://github.com/mauricelambert/LocalResolver/"

copyright = """
LocalResolver  Copyright (C) 2021, 2023  Maurice Lambert
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions.
"""
__license__ = license
__copyright__ = copyright

__all__ = [
    "ResolveNetbios",
]

print(copyright)

from scapy.all import (
    DNSQR,
    DNSRR,
    LLMNRQuery,
    LLMNRResponse,
    IP,
    IPv6,
    UDP,
    NBNSQueryRequest,
    NBNSHeader,
    Raw,
    sr1,
    send,
    AsyncSniffer,
)
from time import sleep
from ipaddress import ip_address
from argparse import ArgumentParser
from socket import gethostbyaddr, gaierror, herror, gethostbyname_ex


class ResolveNetbios:
    def __init__(self, ip, timeout=3):
        self.ip = ip
        self.nom = None
        self.timeout = timeout

    def resolve_NBTNS(self):
        response = sr1(
            IP(dst=self.ip)
            / UDP(sport=137, dport=137)
            / NBNSHeader(QDCOUNT=1, NM_FLAGS=0) / NBNSQueryRequest(
                QUESTION_NAME="*" + "\x00" * 14, QUESTION_TYPE=33
            ),
            timeout=self.timeout,
            verbose=0,
        )

        if response and response.haslayer(Raw):
            self.nom = ""
            for car in response[Raw].load:
                car = chr(car)
                if car == " " or (car == "\x00" and len(self.nom)):
                    return self.nom
                elif car in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-":
                    self.nom += car
        else:
            return None

    def resolve_LLMNR(self):
        self.no_LLMNRResponse = True
        name = ".".join(self.ip.split(".")[::-1]) + ".in-addr.arpa."

        sniffer = AsyncSniffer(
            filter="port 5355 and proto UDP",
            prn=lambda packet: self.check_LLMNR(packet, name),
        )
        sniffer.start()

        self.send_LLMNRQuery(name)
        sniffer.stop()

        if not self.no_LLMNRResponse:
            return self.nom

    def send_LLMNRQuery(self, name):
        for a in range(5):
            send(
                IP(dst="224.0.0.252")
                / UDP(dport=5355)
                / LLMNRQuery(qdcount=1, qd=DNSQR(qtype=12, qname=name)),
                verbose=0,
            )
            send(
                IPv6(dst="ff02::1:3")
                / UDP(dport=5355)
                / LLMNRQuery(qdcount=1, qd=DNSQR(qtype=12, qname=name)),
                inter=1,
                count=2,
                verbose=0,
            )
            if not self.no_LLMNRResponse:
                break

        if self.no_LLMNRResponse:
            sleep(self.timeout)

    def check_LLMNR(self, packet, name):
        if packet.haslayer(LLMNRResponse) and packet.haslayer(DNSRR):
            if packet[DNSRR].rrname == name.encode():
                self.no_LLMNRResponse = False
                self.nom = packet[DNSRR].rdata.decode()

def parse():
    parser = ArgumentParser()
    parser.add_argument(
        "IP_HOSTNAMES",
        help="IP or hostnames to resolve (example: 192.168.1.2,Windows10,HOME-PC).",
    )
    return parser.parse_args()


def is_ip(ip_hostname):
    try:
        ip_address(ip_hostname)
    except ValueError:
        return False
    else:
        return True


def socket_resolver(ip_hostname):
    try:
        hostname, alias, ip = gethostbyaddr(ip_hostname)
    except gaierror:
        pass
    except herror:
        pass
    else:
        return hostname, alias, ip

    try:
        hostname, alias, ip = gethostbyname_ex(ip_hostname)
    except gaierror:
        return
    except herror:
        return
    else:
        return hostname, alias, ip


def resolve_local_ip(ip):
    netbios = ResolveNetbios(ip)
    hostname = netbios.resolve_NBTNS()
    if not hostname:
        hostname = netbios.resolve_LLMNR()
    return hostname or ""


def main():
    parser = parse()
    ip_hostnames = parser.IP_HOSTNAMES.split(",")

    for ip_hostname in ip_hostnames:
        print(f"\nResolve {ip_hostname}...")
        hostname, alias, ip = None, None, None

        resolve = socket_resolver(ip_hostname)

        if (not resolve or resolve[0] == resolve[2][0]) and is_ip(ip_hostname):
            hostname, ip, alias = resolve_local_ip(ip_hostname), ip_hostname, None
        elif resolve:
            hostname, alias, ip = resolve
            alias = ", ".join(alias)
            ip = ", ".join(ip)
        else:
            print(f"\t - Hostname: {ip_hostname} can't be result.")

        if hostname:
            print(f"\t - Hostname for {ip_hostname}: {hostname}")
        if ip:
            print(f"\t - IP for {ip_hostname}: {ip}")
        if alias:
            print(f"\t - Alias for {ip_hostname}: {alias}")


def resolve_all(results, ip_hostname):
    resolve = socket_resolver(ip_hostname)

    hostname, alias, ip = "", "", ""

    if (not resolve or resolve[0] == resolve[2][0]) and is_ip(ip_hostname):
        hostname, ip = resolve_local_ip(ip_hostname), ip_hostname
    elif resolve:
        hostname, alias, ip = resolve
        alias = ", ".join(alias)
        ip = ", ".join(ip)

    results[ip_hostname] = (hostname, alias, ip)


def main_thread():
    from threading import Thread, enumerate, current_thread

    parser = parse()
    ip_hostnames = parser.IP_HOSTNAMES.split(",")
    results = {}

    for ip_hostname in ip_hostnames:
        Thread(
            target=resolve_all,
            args=(
                results,
                ip_hostname,
            ),
        ).start()

    current = current_thread()
    for thread in enumerate():
        if current is not thread:
            thread.join()

    for ip_hostname, results_ in results.items():
        print(
            f"\nQuery: {ip_hostname}\n\t - Hostname: {results_[0]}\n\t - Alias: {results_[1]}\n\t - IP: {results_[2]}"
        )



if __name__ == "__main__":
    main_thread()

