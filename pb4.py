from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

def topology():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='50,50,0', ip='10.0.0.254/24')
    s1 = net.addStation('sta1', position='10,40,0', ip='10.0.0.1/24')
    s2 = net.addStation('sta2', position='20,40,0', ip='10.0.0.2/24')
    s3 = net.addStation('sta3', position='30,40,0', ip='10.0.0.3/24')
    s4 = net.addStation('sta4', position='40,40,0', ip='10.0.0.4/24')
    s5 = net.addStation('sta5', position='50,40,0', ip='10.0.0.5/24')
    server = net.addHost('server', ip='10.0.0.100/24')
    c1 = net.addController('c1')

    info("*** Configuring wifi nodes\n")
    net.setPropagationModel(model="logDistance", exp=4)
    net.configureWifiNodes()

    info("*** Creating links\n")
    net.addLink(ap1, server)  # wired link between AP and server

    info("*** Starting network\n")
    net.build()
    c1.start()
    ap1.start([c1])

    info("*** Network is up. CLI is starting.\n")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

