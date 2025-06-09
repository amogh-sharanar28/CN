from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mininet.node import Controller
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference


def topology():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', ip='10.0.0.1/8', position='10,20,0', ieee80211n='no', ieee80211g='no')  # 802.11a
    sta2 = net.addStation('sta2', ip='10.0.0.2/8', position='20,30,0', ieee80211n='no', ieee80211a='no')  # 802.11g
    sta3 = net.addStation('sta3', ip='10.0.0.3/8', position='30,40,0', ieee80211a='no', ieee80211g='no')  # 802.11n
    ap1 = net.addAccessPoint('ap1', ssid="test-ssid", mode="g", channel="1", position='20,20,0')
    c1 = net.addController('c1')

    info("*** Configuring WiFi nodes\n")
    net.configureWifiNodes()

    # Optional: visualize and confirm coverage
    net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    info("*** Waiting for association\n")
    net.waitConnected(timeout=5)

    info("*** Running Ping Test\n")
    net.ping([sta1, sta2, sta3])

    info("*** Starting iperf servers\n")
    sta1.cmd('iperf -s -u -i 1 > sta1_iperf.txt &')
    sta2.cmd('iperf -s -u -i 1 > sta2_iperf.txt &')
    sta3.cmd('iperf -s -u -i 1 > sta3_iperf.txt &')

    info("*** Running iperf clients (UDP)\n")
    sta1.cmd('iperf -c 10.0.0.1 -u -b 20M -t 10')
    sta2.cmd('iperf -c 10.0.0.2 -u -b 20M -t 10')
    sta3.cmd('iperf -c 10.0.0.3 -u -b 40M -t 10')

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()