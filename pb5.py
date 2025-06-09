from mininet.node import Controller
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

def topology():
    net = Mininet_wifi(controller=Controller, link=wmediumd, wmediumd_mode=interference)

    print("*** Creating nodes with fixed tx rate and IPs")
    sta1 = net.addStation('sta1', ip='10.0.0.1/24', position='10,40,0', mode='g', txrate='54Mbps')
    sta2 = net.addStation('sta2', ip='10.0.0.2/24', position='20,40,0', mode='g', txrate='54Mbps')
    ap1 = net.addAccessPoint('ap1', ssid='ssid-ap1', mode='g', channel='1', position='50,50,0', txrate='54Mbps')
    server = net.addHost('server', ip='10.0.0.100/24')
    c1 = net.addController('c1')

    print("*** Configuring WiFi nodes")
    net.setPropagationModel(model="logDistance", exp=4)
    net.configureWifiNodes()

    print("*** Creating link between AP and server")
    net.addLink(ap1, server)

    print("*** Starting network")
    net.build()
    c1.start()
    ap1.start([c1])

    print("*** Launch CLI to test")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    topology()

