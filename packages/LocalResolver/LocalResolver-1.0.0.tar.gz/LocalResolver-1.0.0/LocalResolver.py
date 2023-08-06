#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###################
#    This module implements local hostname resolver tool with scapy.
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
This module implements local hostname resolver tool with scapy.

Useful wireshark filter:
 - udp.port == 53 || udp.port == 5355 || udp.port == 5353 || udp.port == 137

Linux tools/services to resolve hostname:
~# sudo apt install samba
~# sudo nano /etc/samba/smb.conf
[global]
   netbios name = MYHOST
   workgroup = MYGROUP
   wins support = yes
   name resolve order = lmhosts wins bcast host
~# sudo apt install avahi-daemon  # MDNS
~# sudo apt install systemd-resolved # LLMNR
~# sudo nano /etc/systemd/resolved.conf
LLMNR=yes
~# sudo systemctl restart winbind
~# sudo systemctl restart systemd-resolved
~# sudo systemctl start nmbd
~# sudo systemctl start avahi-daemon
~# sudo responder -I eth0
~# 
"""

__version__ = "1.0.0"
__author__ = "Maurice Lambert"
__author_email__ = "mauricelambert434@gmail.com"
__maintainer__ = "Maurice Lambert"
__maintainer_email__ = "mauricelambert434@gmail.com"
__description__ = (
    "This package implements local hostname resolver tool with scapy."
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
    "LocalResolver",
    "resolve_local_ip",
    "resolve_local_name",
    "Result",
    "netbios_encode",
    "netbios_decode",
]

print(copyright)

from scapy.all import (
    NBNSNodeStatusResponse,
    NBNSNodeStatusRequest,
    NBNSQueryResponse,
    NBNSQueryRequest,
    LLMNRResponse,
    AsyncSniffer,
    NBNSHeader,
    LLMNRQuery,
    RandShort,
    DNSRROPT,
    IFACES,
    Packet,
    DNSQR,
    IPv6,
    conf,
    send,
    ltoa,
    UDP,
    DNS,
    raw,
    IP,
)
from ipaddress import (
    ip_address,
    IPv6Address,
    IPv4Address,
    IPv4Network,
    IPv6Network,
)
from threading import Thread, enumerate as thread_enumeration, current_thread
from socket import gethostbyaddr, gaierror, herror, gethostbyname_ex
from PythonToolsKit.Arguments import ArgumentParser, verbose
from typing import Dict, List, Set, Tuple, Iterable
from PythonToolsKit.PrintF import printf
from collections.abc import Callable
from logging import getLogger, ERROR
from collections import defaultdict
from dataclasses import dataclass
from argparse import Namespace
from os import name

is_windows: bool = name == "nt"


def netbios_encode(name: str) -> str:
    """
    This function encodes name in Netbios encoding.

    >>> netbios_encode('FRED')
    'EGFCEFEECACACACACACACACACACACACA'
    >>> netbios_encode('*')
    'CKCACACACACACACACACACACACACACACA'
    >>>
    """

    encoded_name = bytearray()

    for char in name.encode("ascii"):
        encoded_name.append((char >> 4) + 65)
        encoded_name.append((char & 0xF) + 65)

    encoded_name.extend(b"CA" * (16 - len(name)))
    return encoded_name.decode("ascii")


def netbios_decode(encoded_name: str) -> str:
    """
    This function encodes name in Netbios encoding.

    >>> netbios_decode('EGFCEFEECACACACACACACACACACACACA')
    'FRED'
    >>> netbios_decode('CKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    '*'
    >>>
    """

    name = bytearray()
    encoded_name = encoded_name.encode("ascii")

    for i in range(0, len(encoded_name), 2):
        h = (encoded_name[i] - 65) << 4
        l = encoded_name[i + 1] - 65
        name.append(h | l)

    return name.decode("ascii").rstrip(" \x00")


def reverse_reverse_pointer(reverse_pointer: str) -> str:
    """
    This function reverses reverse pointer to IP address.

    >>> reverse_reverse_pointer("1.0.168.192.in-addr.arpa")
    '192.168.0.1'
    >>> reverse_reverse_pointer("1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.8.b.d.0.1.0.0.2.ip6.arpa")
    '2001:db8::1'
    >>>
    """

    if reverse_pointer.endswith(".in-addr.arpa."):
        return ".".join(reverse_pointer.split(".")[::-1][3:])
    elif reverse_pointer.endswith(".ip6.arpa."):
        reverse_chars = reverse_pointer.split(".")[::-1][3:]
        return str(
            IPv6Address(
                ":".join(
                    [
                        "".join(reverse_chars[i : i + 4])
                        for i in range(0, len(reverse_chars), 4)
                    ]
                )
            )
        )

    return reverse_pointer


@dataclass
class Result:
    source: str
    ip: str
    hostname: str
    type_: str

    def __hash__(self):
        return hash(self.source + self.ip + self.hostname + self.type_)


class LocalResolver:

    """
    This class resolve hostname using Netbios, LLMNR, MDNS and DNS.
    """

    def __init__(
        self,
        name: str = None,
        ip: str = None,
        retry: int = 2,
        inter: int = 1,
        timeout: int = 3,
    ):
        self.retry = retry
        self.inter = inter
        self.ip: str = ip
        self.name: str = name
        self.ips: Set[Result] = set()
        self.names: Set[Result] = set()
        self.timeout: int = timeout
        my_ip_v4s = self.my_ip_v4s = {
            ip: (interface, route)
            for interface in IFACES.data.values()
            for ip in interface.ips[4]
            for route in conf.route.routes
            if route[1] != 4294967295
            and IPv4Address(ip)
            in IPv4Network("%s/%s" % (ltoa(route[0]), ltoa(route[1])))
        }
        my_ip_v6s = self.my_ip_v6s = {
            ip: (interface, route)
            for interface in IFACES.data.values()
            for ip in interface.ips[6]
            for route in conf.route6.routes
            if IPv6Address(ip) in IPv6Network("%s/%i" % (route[0], route[1]))
        }
        my_ips = self.my_ips = my_ip_v4s.copy()
        my_ips.update(my_ip_v6s)
        self.gateway_ip: str = conf.route.route("0.0.0.0")[2]
        self.gateway_ipv6: str = conf.route6.route("::/0")[2]
        self._handle_response: Callable = None
        self.threads: List[Thread] = []
        self.counter: int = 0
        self.ids: Dict[str, Dict[int, Callable]] = defaultdict(
            lambda: defaultdict(lambda: lambda *x, **y: None)
        )

    if is_windows:

        def sniff(self) -> None:
            """
            This function starts sniffer.
            """

            for iface, _ in self.my_ips.values():
                sniffer = AsyncSniffer(
                    filter=(
                        "proto UDP and (port 137 or port 5355"
                        " or port 5353 or port 53)"
                    ),
                    timeout=self.timeout,
                    prn=self.redirect,
                    iface=iface,  # all interfaces
                )
                sniffer.start()

    else:

        def sniff(self) -> None:
            """
            This function starts sniffer.
            """

            sniffer = self.sniffer = AsyncSniffer(
                filter=(
                    "proto UDP and (port 137 or port 5355"
                    " or port 5353 or port 53)"
                ),
                timeout=self.timeout,
                prn=self.redirect,
                iface=None,  # all interfaces
            )
            sniffer.start()

    def redirect(self, packet: Packet) -> None:
        """
        This function calls callbacks for sniffed packets.
        """

        source = packet[1].src
        if source in self.my_ips:
            return None

        udp = packet[UDP]
        port = udp.sport
        if port == 137:
            self.ids["netbios"][
                NBNSHeader(raw(packet[UDP].payload)).NAME_TRN_ID
            ](packet)
        elif port == 5355:
            self.ids["llmnr"][int.from_bytes(raw(udp.payload)[:2], "big")](
                packet
            )
        elif port == 5353 and (
            (
                self.ip
                and ip_address(self.ip).reverse_pointer.encode("latin-1")
                in raw(packet)
            )
            or (self.name and self.name.encode("latin-1") in raw(packet))
        ):
            (
                self.parse_mdns_ip_response
                if self.ip
                else self.parse_mdns_name_response
            )(packet)
        elif port == 53 and packet[DNS].an:
            self.ids["dns"][int.from_bytes(raw(udp.payload)[:2], "big")](
                packet
            )

    def sender(self, packet: Packet) -> str:
        """
        This function sends a query.
        """

        send(
            packet,
            verbose=0,
            count=self.retry,
            inter=self.inter,
            iface=self.my_ips[packet[0].src][0],
        )

    def resolve_netbios_name(self, callback: Callable = None) -> None:
        """
        This function sends the Netbios queries
        requests to get IP address from hostname.
        """

        for ip, (interface, route) in self.my_ip_v4s.items():
            self.counter += 1
            verbose(f"Send new Netbios name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["netbios"][id_] = (
                callback or self.parse_netbios_name_response
            )
            thread = Thread(
                name=f"[{ip}] Netbios name: " + self.name,
                target=self.sender,
                args=(
                    IP(
                        dst=str(
                            IPv4Network(
                                "%s/%s" % (ltoa(route[0]), ltoa(route[1]))
                            ).broadcast_address
                        ),
                        src=ip,
                    )
                    / UDP(sport=137, dport=137)
                    / NBNSHeader(NAME_TRN_ID=id_, QDCOUNT=1, NM_FLAGS=0x011)
                    / NBNSQueryRequest(
                        QUESTION_NAME=self.name, QUESTION_TYPE=32
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

    def resolve_netbios_ip(self, callback: Callable = None) -> None:
        """
        This function sends the Netbios queries
        requests to get hostname from IP address.
        """

        # IP()/UDP(sport=137, dport=137)/NBNSHeader()/NBNSNodeStatusRequest(QUESTION_NAME=b'*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', QUESTION_TYPE=33)

        if not isinstance(ip_address(self.ip), IPv4Address):
            return None

        for ip in self.my_ip_v4s:
            self.counter += 1
            verbose(f"Send new Netbios IP query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["netbios"][id_] = (
                callback or self.parse_netbios_ip_response
            )
            thread = Thread(
                name=f"[{ip}] Netbios IP: " + self.ip,
                target=self.sender,
                args=(
                    IP(dst=self.ip, src=ip)
                    / UDP(sport=137, dport=137)
                    / NBNSHeader(
                        NAME_TRN_ID=RandShort(), QDCOUNT=1, NM_FLAGS=0
                    )
                    / NBNSNodeStatusRequest(
                        QUESTION_NAME="*" + "\x00" * 14, QUESTION_TYPE=33
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

    def resolve_llmnr_ip(self, callback: Callable = None) -> None:
        """
        This function sends the LLMNR queries
        requests to get hostname from IP address.
        """

        # IPv6(dst='ff02::1:3')/UDP(sport=55173, dport=5355)/LLMNRQuery(qd=DNSQR(qname=b'X.X.X.ip6.arpa.', qtype=12))

        name = ip_address(self.ip).reverse_pointer

        for ip in self.my_ip_v4s:
            self.counter += 1
            verbose(f"Send new LLMNR IP query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["llmnr"][id_] = callback or self.parse_llmnr_ip_response
            thread = Thread(
                name=f"[{ip}] LLMNR IP: " + self.ip,
                target=self.sender,
                args=(
                    IP(dst="224.0.0.252", src=ip)
                    / UDP(dport=5355)
                    / LLMNRQuery(
                        id=id_,
                        qdcount=1,
                        qd=DNSQR(qtype=12, qname=name),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

        for ip in self.my_ip_v6s:
            self.counter += 1
            verbose(f"Send new IPv6/LLMNR IP query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["llmnr"][id_] = callback or self.parse_llmnr_ip_response
            thread = Thread(
                name=f"[{ip}] LLMNR IP: " + self.ip,
                target=self.sender,
                args=(
                    IPv6(dst="ff02::1:3")
                    / UDP(dport=5355)
                    / LLMNRQuery(
                        id=id_,
                        qdcount=1,
                        qd=DNSQR(qtype=12, qname=name),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

    def resolve_llmnr_name(self, callback: Callable = None) -> None:
        """
        This function sends the LLMNR queries
        requests to get IP address from hostname.
        """

        for ip in self.my_ip_v4s:
            self.counter += 1
            verbose(f"Send new LLMNR name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["llmnr"][id_] = callback or self.parse_llmnr_name_response
            thread = Thread(
                name=f"[{ip}] LLMNR name: " + self.name,
                target=self.sender,
                args=(
                    IP(dst="224.0.0.252", src=ip)
                    / UDP(dport=5355)
                    / LLMNRQuery(
                        id=id_,
                        qdcount=1,
                        qd=DNSQR(qtype=1, qname=self.name),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

        for ip in self.my_ip_v6s:
            self.counter += 1
            verbose(f"Send new IPv6/LLMNR name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["llmnr"][id_] = callback or self.parse_llmnr_name_response
            thread = Thread(
                name=f"[{ip}] LLMNR name: " + self.name,
                target=self.sender,
                args=(
                    IPv6(dst="ff02::1:3")
                    / UDP(dport=5355)
                    / LLMNRQuery(
                        id=id_,
                        qdcount=1,
                        qd=DNSQR(qtype=28, qname=self.name),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

    def resolve_mdns_ip(self, callback: Callable = None) -> None:
        """
        This function sends the MDNS queries
        requests to get name from IP address.
        """

        name = ip_address(self.ip).reverse_pointer

        for ip in self.my_ip_v4s:
            self.counter += 1
            verbose(f"Send new MDNS IP query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["mdns"][id_] = callback or self.parse_mdns_ip_response
            thread = Thread(
                name=f"[{ip}] MDNS IP: " + self.ip,
                target=self.sender,
                args=(
                    IP(dst="224.0.0.252", src=ip)
                    / UDP(dport=5353)
                    / DNS(id=id_, rd=1, qd=DNSQR(qtype=12, qname=name)),
                ),
            )

            self.threads.append(thread)
            thread.start()

        for ip in self.my_ip_v6s:
            self.counter += 1
            verbose(f"Send new IPv6/MDNS IP query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["mdns"][id_] = callback or self.parse_mdns_ip_response
            thread = Thread(
                name=f"[{ip}] MDNS IP: " + self.ip,
                target=self.sender,
                args=(
                    IPv6(dst="ff02::1:3")
                    / UDP(dport=5355)
                    / DNS(id=id_, rd=1, qd=DNSQR(qtype=12, qname=name)),
                ),
            )

            self.threads.append(thread)
            thread.start()

    def resolve_mdns_name(self, callback: Callable = None) -> None:
        """
        This function sends the MDNS queries
        requests to get IP address from name.
        """

        # IP(dst='224.0.0.251')/UDP(sport=5353, dport=5353)/DNS(qd=DNSQR(qname=b'XXXX.local.', qtype=1))

        for ip in self.my_ip_v4s:
            self.counter += 1
            verbose(f"Send new MDNS name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["mdns"][id_] = callback or self.parse_mdns_name_response
            thread = Thread(
                name=f"[{ip}] MDNS name: " + self.name,
                target=self.sender,
                args=(
                    IP(dst="224.0.0.251", src=ip)
                    / UDP(sport=RandShort(), dport=5353)
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=1, qname=self.name),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

        for ip in self.my_ip_v6s:
            self.counter += 1
            verbose(f"Send new IPv6/MDNS name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["mdns"][id_] = callback or self.parse_mdns_name_response
            thread = Thread(
                name=f"[{ip}] MDNS name: " + self.name,
                target=self.sender,
                args=(
                    IPv6(dst="ff02::1:3")
                    / UDP(dport=5353)
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=28, qname=self.name),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

    def resolve_dns_ip(self, callback: Callable = None) -> None:
        """
        This function sends the DNS queries
        requests to get name from IP address.
        """

        # IP()/UDP(dport=53, sport=RandShort())/DNS(qd=DNSQR(qname=b'XX.XX.XX.XX.in-addr.arpa.', qtype=12), ar=DNSRROPT(rrname=b'.', type=41))

        name = ip_address(self.ip).reverse_pointer

        for ip in self.my_ip_v4s:
            self.counter += 1
            verbose(f"Send new DNS IP query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["dns"][id_] = callback or self.parse_dns_ip_response
            thread = Thread(
                name=f"[{ip}] DNS IP: " + self.ip,
                target=self.sender,
                args=(
                    IP(dst=self.gateway_ip, src=ip)
                    / UDP(dport=53, sport=RandShort())
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=12, qname=name),
                        ar=DNSRROPT(rrname=b".", type=41),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

        for ip in self.my_ip_v6s:
            self.counter += 1
            verbose(f"Send new DNS IP query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["dns"][id_] = callback or self.parse_dns_ip_response
            thread = Thread(
                name=f"[{ip}] DNS IP: " + self.ip,
                target=self.sender,
                args=(
                    IPv6(dst=self.gateway_ipv6, src=ip)
                    / UDP(dport=53, sport=RandShort())
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=12, qname=name),
                        ar=DNSRROPT(rrname=b".", type=41),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

    def resolve_dns_name(self, callback: Callable = None) -> None:
        """
        This function sends the DNS queries
        requests to get IP address from name.
        """

        # IP()/UDP(dport=53, sport=RandShort())/DNS(qd=DNSQR(qname=b'XXXX.home.', qtype=1), ar=DNSRROPT(rrname=b'.', type=41))

        for ip in self.my_ip_v4s:
            self.counter += 1
            verbose(f"Send new DNS name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["dns"][id_] = callback or self.parse_dns_name_response
            thread = Thread(
                name=f"[{ip}] DNS name: " + self.name,
                target=self.sender,
                args=(
                    IP(dst=self.gateway_ip, src=ip)
                    / UDP(dport=53, sport=RandShort())
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=1, qname=self.name),
                        ar=DNSRROPT(rrname=b".", type=41),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

            self.counter += 1
            verbose(f"Send new DNS name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["dns"][id_] = callback or self.parse_dns_name_response
            thread = Thread(
                name=f"[{ip}] DNS name: " + self.name + ".home",
                target=self.sender,
                args=(
                    IP(dst=self.gateway_ip, src=ip)
                    / UDP(dport=53, sport=RandShort())
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=1, qname=self.name + ".home"),
                        ar=DNSRROPT(rrname=b".", type=41),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

            self.counter += 1
            verbose(f"Send new DNS name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["dns"][id_] = callback or self.parse_dns_name_response
            thread = Thread(
                name=f"[{ip}] DNS name: " + self.name + ".home.arpa",
                target=self.sender,
                args=(
                    IP(dst=self.gateway_ip, src=ip)
                    / UDP(dport=53, sport=RandShort())
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=1, qname=self.name + ".home.arpa"),
                        ar=DNSRROPT(rrname=b".", type=41),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

        for ip in self.my_ip_v6s:
            self.counter += 1
            verbose(f"Send new IPv6/DNS name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["dns"][id_] = callback or self.parse_dns_name_response
            thread = Thread(
                name=f"[{ip}] DNS name: " + self.name,
                target=self.sender,
                args=(
                    IPv6(dst=self.gateway_ipv6, src=ip)
                    / UDP(dport=53, sport=RandShort())
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=28, qname=self.name),
                        ar=DNSRROPT(rrname=b".", type=41),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

            self.counter += 1
            verbose(f"Send new IPv6/DNS name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["dns"][id_] = callback or self.parse_dns_name_response
            thread = Thread(
                name=f"[{ip}] DNS name: " + self.name + ".home",
                target=self.sender,
                args=(
                    IPv6(dst=self.gateway_ipv6, src=ip)
                    / UDP(dport=53, sport=RandShort())
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=28, qname=self.name + ".home"),
                        ar=DNSRROPT(rrname=b".", type=41),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

            self.counter += 1
            verbose(f"Send new IPv6/DNS name query (packet: {self.counter})")
            id_ = int(RandShort()) ^ self.counter
            self.ids["dns"][id_] = callback or self.parse_dns_name_response
            thread = Thread(
                name=f"[{ip}] DNS name: " + self.name + ".home.arpa",
                target=self.sender,
                args=(
                    IPv6(dst=self.gateway_ipv6, src=ip)
                    / UDP(dport=53, sport=RandShort())
                    / DNS(
                        id=id_,
                        rd=1,
                        qd=DNSQR(qtype=28, qname=self.name + ".home.arpa"),
                        ar=DNSRROPT(rrname=b".", type=41),
                    ),
                ),
            )

            self.threads.append(thread)
            thread.start()

    def parse_netbios_name_response(self, packet: Packet) -> str:
        """
        This method parses netbios response and returns IP address.
        """

        # IP()/UDP(sport=137, dport=137)/NBNSHeader()/NBNSQueryResponse(ADDR_ENTRY=[NBNS_ADD_ENTRY(NB_ADDRESS='XX.XX.XX.XX')], RR_NAME=b'XXXX           ', QUESTION_TYPE=32)

        response = NBNSQueryResponse(
            raw(NBNSHeader(raw(packet[UDP].payload)).payload)
        )

        source = packet[1].src
        name = response.RR_NAME.decode("latin-1")
        ips = ", ".join(x.NB_ADDRESS for x in response.ADDR_ENTRY)
        self.ips.add(Result(source, ips, name, "Netbios"))

        if self._handle_response:
            self._handle_response(source, ips, name)

        return ips

    def parse_netbios_ip_response(self, packet: Packet) -> str:
        """
        This method parses netbios response and returns name.
        """

        # IP()/UDP(sport=137, dport=137)/NBNSHeader()/NBNSNodeStatusResponse(NODE_NAME=[
        #     NBNSNodeStatusResponseService(NETBIOS_NAME=b'XXXX           '),
        #     NBNSNodeStatusResponseService(NETBIOS_NAME=b'XXXX           '),
        #     NBNSNodeStatusResponseService(NETBIOS_NAME=b'XXXX           '),
        #     NBNSNodeStatusResponseService(NETBIOS_NAME=b'WORKGROUP      ', SUFFIX=1, NAME_FLAGS=132),
        #     NBNSNodeStatusResponseService(NETBIOS_NAME=b'WORKGROUP      ', NAME_FLAGS=132),
        #     NBNSNodeStatusResponseService(NETBIOS_NAME=b'WORKGROUP      ', SUFFIX=29),
        #     NBNSNodeStatusResponseService(NETBIOS_NAME=b'WORKGROUP      ', SUFFIX=30, NAME_FLAGS=132)
        # ], RR_NAME=b'*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', RR_TYPE=33)

        response = NBNSNodeStatusResponse(
            raw(NBNSHeader(raw(packet[UDP].payload)).payload)
        )
        source = packet[1].src
        names = ", ".join(
            x.NETBIOS_NAME.decode("latin-1") for x in response.NODE_NAME
        )
        self.names.add(Result(source, self.ip, names, "Netbios"))

        if self._handle_response:
            self._handle_response(source, self.ip, names)

        return names

    def parse_llmnr_name_response(self, packet: Packet) -> str:
        """
        This method parses LLMNR response and returns IP address.
        """

        # IP()/UDP(sport=5355, dport=5355)/LLMNRResponse(qd=DNSQR(qname=b'XXXX.'), an=DNSRR(rrname=b'XXXX.', rdata='XX.XX.XX.XX'))

        response = LLMNRResponse(raw(packet[UDP].payload))
        source = packet[1].src
        names = f"{response.qd.qname.decode('latin-1')}, {response.an.rrname.decode('latin-1')}"
        ip = response.an.rdata
        self.ips.add(Result(source, ip, names, "LLMNR"))

        if self._handle_response:
            self._handle_response(source, ip, names)

        return ip

    def parse_llmnr_ip_response(self, packet: Packet) -> str:
        """
        This method parses LLMNR response and returns name.
        """

        # IPv6()/UDP(sport=5355)/LLMNRResponse(qd=DNSQR(qname=b'X.X.X.X.ip6.arpa.', qtype=12), an=DNSRR(rrname=b'X.X.X.X.ip6.arpa.', type=12, rdata=b'XXXX.'))

        response = LLMNRResponse(raw(packet[UDP].payload))
        name = response.an.rdata.decode("latin-1")
        source = packet[1].src
        ips = (
            reverse_reverse_pointer(response.qd.qname.decode("latin-1"))
            + ", "
            + reverse_reverse_pointer(response.an.rrname.decode("latin-1"))
        )
        self.names.add(Result(source, ips, name, "LLMNR"))

        if self._handle_response:
            self._handle_response(source, ips, name)

        return name

    def parse_mdns_name_response(self, packet: Packet) -> str:
        """
        This method parses MDNS response and returns IP address.
        """

        # IP()/UDP(sport=5353, dport=5353)/DNS(an=DNSRR(rrname=b'XXXX.local.', type=1, rdata='XX.XX.XX.XX'))

        response = packet[DNS]
        ip = response.an.rdata
        source = packet[1].src
        name = response.an.rrname.decode("latin-1")
        self.ips.add(Result(source, ip, name, "MDNS"))

        if self._handle_response:
            self._handle_response(source, ip, name)

        return ip

    def parse_mdns_ip_response(self, packet: Packet) -> str:
        """
        This method parses MDNS response and returns name.
        """

        # IP()/UDP(sport=5353)/DNS(qd=DNSQR(qname=b'XX.XX.XX.XX.in-addr.arpa.', qtype=12), an=DNSRR(rrname=b'XX.XX.XX.XX.in-addr.arpa.', type=12, rdata=b'XXXX.local.'))

        response = packet[DNS]
        name = response.an.rdata.decode("latin-1")
        source = packet[1].src
        ips = (
            reverse_reverse_pointer(response.qd.qname.decode("latin-1"))
            + ", "
            + reverse_reverse_pointer(response.an.rrname.decode("latin-1"))
        )
        self.names.add(Result(source, ips, name, "MDNS"))

        if self._handle_response:
            self._handle_response(source, ips, name)

        return name

    def parse_dns_name_response(self, packet: Packet) -> str:
        """
        This method parses DNS response and returns IP address.
        """

        # IP()/UDP(sport=53)/DNS(qd=DNSQR(qname=b'XXXX.home.', qtype=1), an=DNSRR(rrname=b'XXXX.home.', type=1, rdata='XX.XX.XX.XX'), ar=DNSRROPT(rrname=b'.', type=41))

        response = packet[DNS]
        ip = response.an.rdata
        source = packet[1].src
        name = (
            response.qd.qname.decode("latin-1")
            + ", "
            + response.an.rrname.decode("latin-1")
        )
        self.ips.add(Result(source, ip, name, "DNS"))

        if self._handle_response:
            self._handle_response(source, ip, name)

        return ip

    def parse_dns_ip_response(self, packet: Packet) -> str:
        """
        This method parses DNS response and returns name.
        """

        # IP()/UDP(sport=53)/DNS(qd=DNSQR(qname=b'XX.XX.XX.XX.in-addr.arpa.', qtype=12), an=DNSRR(rrname=b'XX.XX.XX.XX.in-addr.arpa.', type=12, rdata=b'XXXX.'), ar=DNSRROPT(rrname=b'.', type=41))

        response = packet[DNS]
        name = response.an.rdata.decode("latin-1")
        source = packet[1].src
        ips = (
            reverse_reverse_pointer(response.qd.qname.decode("latin-1"))
            + ", "
            + reverse_reverse_pointer(response.an.rrname.decode("latin-1"))
        )
        self.names.add(Result(source, ips, name, "DNS"))

        if self._handle_response:
            self._handle_response(source, ips, name)

        return name

    def wait_threads(self) -> None:
        """
        This method waits all LocalResolver threads.
        """

        for thread in self.threads:
            thread.join()


def parse() -> Namespace:
    """
    This function parses command line arguments.
    """

    parser = ArgumentParser(
        description=(
            "This module implements local hostname resolver"
            " tool with scapy (using netbios and LLMNR query)."
        )
    )
    parser.add_verbose()
    parser.add_argument(
        "ip_hostnames",
        nargs="+",
        help="IP or hostnames to resolve.",
    )
    parser.add_argument(
        "--no-llmnr",
        "-l",
        action="store_true",
        help="Don't use LLMNR protocol",
    )
    parser.add_argument(
        "--no-netbios",
        "-n",
        action="store_true",
        help="Don't use Netbios protocol",
    )
    parser.add_argument(
        "--no-mdns",
        "-m",
        action="store_true",
        help="Don't use MDNS protocol",
    )
    parser.add_argument(
        "--no-dns",
        "-d",
        action="store_true",
        help="Don't use DNS protocol",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=3,
        help="Change the timeout to get response.",
    )
    parser.add_argument(
        "--retry",
        "-r",
        type=int,
        default=2,
        help=(
            "How many time you want to retry"
            " if you don't have any response."
        ),
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=1,
        help="Interval between retry.",
    )
    return parser.parse_args()


def is_ip(ip_hostname: str) -> bool:
    """
    THis function checks the
    parameter is an IP address.
    """

    try:
        ip_address(ip_hostname)
    except ValueError:
        return False
    return True


def system_resolver(
    ip_hostname: str, resolver: LocalResolver, callback: Callable = None
) -> Tuple[str, List[str], List[str]]:
    """
    This function uses the system resolve tools.
    """

    resolved = False

    try:
        hostname, alias, ip = gethostbyaddr(ip_hostname)
    except (gaierror, herror):
        pass
    else:
        resolved = True

    try:
        hostname, alias, ip = gethostbyname_ex(ip_hostname)
    except (gaierror, herror):
        pass
    else:
        resolved = True

    if resolved:
        callback is not None and callback(hostname, alias, ip)
        resolver.names.add(
            Result(
                "Unknow",
                ", ".join(ip),
                (", ".join(alias) + ", " + hostname if alias else hostname),
                "System",
            )
        )
        resolver.ips.add(
            Result(
                "Unknow",
                ", ".join(ip),
                (", ".join(alias) + ", " + hostname if alias else hostname),
                "System",
            )
        )
        return hostname, alias, ip


def resolve_local_ip(
    ip: str,
    retry: int = 2,
    inter: int = 1,
    timeout: int = 3,
    netbios: bool = True,
    llmnr: bool = True,
    mdns: bool = True,
    dns: bool = True,
) -> Iterable[Result]:
    """
    This function use LocalResolver
    to get hostname from IP address.
    """

    resolver = LocalResolver(ip=ip, retry=2, inter=1, timeout=3)
    resolver.sniff()
    netbios and resolver.resolve_netbios_ip()
    llmnr and resolver.resolve_llmnr_ip()
    mdns and resolver.resolve_mdns_ip()
    dns and resolver.resolve_dns_ip()
    resolver.wait_threads()
    return resolver.names


def resolve_local_name(
    hostname: str,
    retry: int = 2,
    inter: int = 1,
    timeout: int = 3,
    netbios: bool = True,
    llmnr: bool = True,
    mdns: bool = True,
    dns: bool = True,
) -> Iterable[Result]:
    """
    This function use LocalResolver
    to get IP address from hostname.
    """

    resolver = LocalResolver(name=hostname, retry=2, inter=1, timeout=3)
    resolver.sniff()
    netbios and resolver.resolve_netbios_name()
    llmnr and resolver.resolve_llmnr_name()
    mdns and resolver.resolve_mdns_name()
    dns and resolver.resolve_dns_name()
    resolver.wait_threads()
    return resolver.ips


def main() -> int:
    """
    This function uses the module from the command line.
    """

    parser = parse()
    getLogger("scapy.runtime").setLevel(ERROR)

    for ip_hostname in parser.ip_hostnames:
        printf(f"Resolve: {ip_hostname!r}", state="INFO", pourcent=0)

        if is_ip(ip_hostname):
            resolver = LocalResolver(
                ip=ip_hostname,
                retry=parser.retry,
                inter=parser.interval,
                timeout=parser.timeout,
            )
            resolver.sniff()
            not parser.no_netbios and resolver.resolve_netbios_ip()
            not parser.no_llmnr and resolver.resolve_llmnr_ip()
            not parser.no_mdns and resolver.resolve_mdns_ip()
            not parser.no_dns and resolver.resolve_dns_ip()
        else:
            resolver = LocalResolver(
                name=ip_hostname,
                retry=parser.retry,
                inter=parser.interval,
                timeout=parser.timeout,
            )
            resolver.sniff()
            not parser.no_netbios and resolver.resolve_netbios_name()
            not parser.no_llmnr and resolver.resolve_llmnr_name()
            not parser.no_mdns and resolver.resolve_mdns_name()
            not parser.no_dns and resolver.resolve_dns_name()

        thread = Thread(
            target=system_resolver, name="system", args=(ip_hostname, resolver)
        )
        thread.start()

        current = current_thread()
        threads = thread_enumeration()
        threads_number = len(threads) - 1
        sniffers = []

        for i, thread in enumerate(threads):
            if "AsyncSniffer" in thread.name:
                sniffers.append(thread)
            elif current is not thread and thread.name != "system":
                printf(
                    f"Resolve: {ip_hostname!r} - [step {i}]" + thread.name,
                    state="INFO",
                    pourcent=round((i + 1) / threads_number * 100),
                )
                thread.join()

        [sniffer.join() for sniffer in sniffers]
        thread.join()
        printf(
            f"Resolve: {ip_hostname!r} - [last step] system",
            state="INFO",
            pourcent=100,
        )

        printf(
            f"Resolve: {ip_hostname}:\n\t - "
            + "\t - ".join(
                f"Source: {r.source!r}; IP address(es): {r.ip!r}; Hostname("
                f"s): {r.hostname!r}; Type: {r.type_!r}\n"
                for r in (
                    resolver.names if is_ip(ip_hostname) else resolver.ips
                )
            ),
            start="\n",
        )

    return 0


if __name__ == "__main__":
    exit(main())
