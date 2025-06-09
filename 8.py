#!/usr/bin/python3

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from time import sleep


def topology():
    net = Mininet_wifi(controller=Controller)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='10,20,0')
    h1 = net.addHost('h1', ip='10.0.0.100')
    s1 = net.addSwitch('s1')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='15,20,0')
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='55,20,0')

    c0 = net.addController('c0')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, s1)
    net.addLink(ap2, s1)
    net.addLink(h1, s1)

    info("*** Starting network\n")
    net.build()
    c0.start()
    s1.start([c0])
    ap1.start([c0])
    ap2.start([c0])

    info("*** Forcing sta1 to connect to ap1 initially\n")
    sta1.cmd('iw dev sta1-wlan0 connect ap1-ssid')
    sleep(3)

    info("*** Sta1 initial link:\n")
    print(sta1.cmd('iw dev sta1-wlan0 link'))

    info("*** Starting iperf server on h1\n")
    h1.cmd('iperf -s -i 1 > throughput.log 2>&1 &')
    sleep(2)

    info("*** Starting iperf client on sta1\n")
    sta1.cmd('iperf -c 10.0.0.100 -t 60 -i 1 > client.log 2>&1 &')

    sleep(10)

    info("*** Moving sta1 near AP2\n")
    sta1.setPosition('50,20,0')
    sleep(5)

    info("*** Forcing disconnect from AP1\n")
    sta1.cmd('iw dev sta1-wlan0 disconnect')
    sleep(2)

    info("*** Connecting sta1 explicitly to AP2\n")
    sta1.cmd('iw dev sta1-wlan0 connect ap2-ssid')
    sleep(5)

    info("*** Sta1 link after reconnect:\n")
    print(sta1.cmd('iw dev sta1-wlan0 link'))

    sleep(35)

    info("*** Test completed, stopping network\n")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    topology()

