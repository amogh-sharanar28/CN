#!/usr/bin/python3

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from time import sleep

def topology():
    "Create a more realistic wireless network."
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Setting realistic propagation model\n")
    # logNormalShadowing introduces fading and path loss; adjust exp and variance for realism
    net.setPropagationModel(model="logNormalShadowing",exp=4)

    info("*** Adding nodes\n")
    sta1 = net.addStation('sta1', position='20,35,0', ip='10.0.0.10/24')
    sta2 = net.addStation('sta2', position='90,35,0', ip='10.0.0.20/24')  # Farther from AP
    ap1 = net.addAccessPoint('ap1', ssid='wifi', mode='g', channel='1', position='45,35,0')
    s1 = net.addSwitch('s1')
    h1 = net.addHost('h1', ip='10.0.0.100/24')
    c1 = net.addController('c1')

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(h1, s1)
    net.addLink(ap1, s1)

    info("*** Building network\n")
    net.build()
    c1.start()
    s1.start([c1])
    ap1.start([c1])

    info("*** Waiting for network to stabilize\n")
    sleep(3)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__== '__main__':
    setLogLevel('info')
    topology()


#iperf sta1 h1
#iperf sta2 h1
#sta1 ping -c 5 sta2
#sta2 ping -c 5 sta1    
#sta1 ping -c 5 ap1
#sta2 ping -c 5 ap1