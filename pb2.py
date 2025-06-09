from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from mininet.log import setLogLevel

def topology():    
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    print("*** Creating nodes")
    sta1 = net.addStation('sta1', position='0,0,0')
    sta2 = net.addStation('sta2', position='140,0,0')
    ap1 = net.addAccessPoint('ap1', ssid='simplewifi', mode='g', channel='1', position='70,0,0', range=50)
    c1 = net.addController('c1')

    print("*** Configuring wifi nodes")
    net.configureWifiNodes()

    print("*** Starting network")
    net.build()
    c1.start()
    ap1.start([c1])

    print("*** Running CLI")
    CLI(net)

    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()


# sta1 ping -c 5 sta2
# sta2 iperf -c sta1
