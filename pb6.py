#!/usr/bin/python3

from mn_wifi.net import Mininet_wifi
from mininet.node import Controller
from time import sleep

def topology():
    net = Mininet_wifi(controller=Controller)

    print("*** Creating nodes")
    sta1 = net.addStation('sta1', position='50,20,0')
    h1 = net.addHost('h1', ip='10.0.0.100')
    s1 = net.addSwitch('s1')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='15,20,0')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='55,20,0')
    c0 = net.addController('c0')

    net.configureWifiNodes()

    net.addLink(ap1, s1)
    net.addLink(ap2, s1)
    net.addLink(h1, s1)

    net.build()
    c0.start()
    s1.start([c0])
    ap1.start([c0])
    ap2.start([c0])

    print("*** Connecting sta1 to AP2")
    sta1.cmd('iw dev sta1-wlan0 connect ap2-ssid')
    sleep(5)
    print(sta1.cmd('iw dev sta1-wlan0 link'))

    print("*** Opening xterm and starting ping to h1")
    sta1.cmd('xterm -hold -e ping -c 30 10.0.0.100 &')
    sleep(5)

    print("*** Moving sta1 towards AP1")
    sta1.setPosition('15,20,0')
    sleep(5)

    print("*** Disconnecting from AP2")
    sta1.cmd('iw dev sta1-wlan0 disconnect')
    sleep(6)

    print("*** Connecting to AP1")
    sta1.cmd('iw dev sta1-wlan0 connect ap1-ssid')
    sleep(5)
    print(sta1.cmd('iw dev sta1-wlan0 link'))
    sleep(10)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    topology()



"""
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
import time
import matplotlib.pyplot as plt
import re


def capture_metrics(sta, ap_ip):
    delay_file = open("delay.txt", "w")
    loss_file = open("packet_loss.txt", "w")

    delay_file.write("Distance,Delay(ms)\n")
    loss_file.write("Distance,Packet Loss(%)\n")

    for x in range(10, 60, 10):  # Moves: 10, 20, 30, 40, 50
        sta.setPosition(f'{x},10,0')
        info(f"*** Moved STA1 to x={x}\n")
        time.sleep(3)

        # Ping 5 packets to AP2
        ping_output = sta.cmd(f'ping -c 5 {ap_ip}')
        match_rtt = re.search(r"rtt min/avg/max/mdev = ([^/])/([^/])", ping_output)
        match_loss = re.search(r"(\d+)% packet loss", ping_output)

        if match_rtt:
            avg_delay = float(match_rtt.group(2))
        else:
            avg_delay = 0.0

        if match_loss:
            loss = float(match_loss.group(1))
        else:
            loss = 100.0

        delay_file.write(f"{x},{avg_delay:.2f}\n")
        loss_file.write(f"{x},{loss:.2f}\n")

    delay_file.close()
    loss_file.close()


def plot_results():
    distances, delays, losses = [], [], []

    with open("delay.txt") as f:
        next(f)
        for line in f:
            x, d = line.strip().split(",")
            distances.append(int(x))
            delays.append(float(d))

    with open("packet_loss.txt") as f:
        next(f)
        for line in f:
            x, l = line.strip().split(",")
            losses.append(float(l))

    # Plot Delay
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.plot(distances, delays, marker='o', color='blue')
    plt.title("RTT Delay During Handover")
    plt.xlabel("STA1 Position (X-axis)")
    plt.ylabel("Average Delay (ms)")
    plt.grid(True)

    # Plot Packet Loss
    plt.subplot(1, 2, 2)
    plt.plot(distances, losses, marker='x', color='red')
    plt.title("Packet Loss During Handover")
    plt.xlabel("STA1 Position (X-axis)")
    plt.ylabel("Packet Loss (%)")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("handover_metrics.png")
    plt.show()


def run_experiment():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating network nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel=1, position='10,20,0')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel=6, position='50,20,0')
    sta1 = net.addStation('sta1', position='10,10,0')
    c0 = net.addController('c0')

    net.configureWifiNodes()
    net.build()
    c0.start()
    ap1.start([c0])
    ap2.start([c0])

    info("*** Starting handover simulation\n")
    sta1.cmd('ping -c 1 127.0.0.1')  # Warm-up

    capture_metrics(sta1, ap2.IP())

    info("*** Running CLI (type 'exit' to quit)\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

    plot_results()


if _name_ == '_main_':
    setLogLevel('info')
    run_experiment()
"""