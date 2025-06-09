from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference
from time import sleep
from mn_wifi.node import OVSKernelAP
def topology():
    net = Mininet_wifi(controller=Controller, accessPoint=OVSKernelAP)

    info("*** Creating nodes\n")
    sta1 = net.addStation('sta1', position='20,50,0')
    ap1 = net.addAccessPoint('ap1', ssid='ap1-ssid', mode='g', channel='1', position='20,60,0', txpower=15)
    ap2 = net.addAccessPoint('ap2', ssid='ap2-ssid', mode='g', channel='6', position='80,50,0', txpower=15)
    c0 = net.addController('c0')

    net.configureWifiNodes()
    net.plotGraph(max_x=100, max_y=100)
    net.start()

    info("*** Waiting for STA to associate with AP1\n")
    sleep(2)

    # Initial connection status
    info('--- Initial Connection ---\n')
    sta1.cmdPrint('iw dev sta1-wlan0 link')

    info('\n*** Gradually reducing txpower of AP1\n')
    for tx in range(14, -1, -1):
        ap1.setTxPower(tx)
        info(f'\n--- TxPower of ap1: {tx} dBm ---\n')
        sta1.cmdPrint('iw dev sta1-wlan0 link')

        if tx == 5:
            info('\n>>> Moved sta1 closer to ap2 <<<\n')
            sta1.setPosition('80,50,0')  # Close to ap2
            sleep(2)

            # Force disconnection
            sta1.cmd('iw dev sta1-wlan0 disconnect')
            sleep(1)

            # Re-scan and try to reconnect
            sta1.cmd('iw dev sta1-wlan0 scan')
            sta1.cmd('iw dev sta1-wlan0 connect ap2-ssid')
            sleep(2)

            info('\n--- After Forcing Reconnection ---\n')
            sta1.cmdPrint('iw dev sta1-wlan0 link')

        sleep(2)

    info('\n*** Starting CLI:\n')
    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

