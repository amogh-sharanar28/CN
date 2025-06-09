from mininet.log import setLogLevel
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import UserAP
import time

def get_bssid(sta):
    out = sta.cmd('iw dev %s-wlan0 link' % sta.name)
    for line in out.splitlines():
        if line.startswith('Connected to'):
            return line.split()[2]
    return None

def topology():
    net = Mininet_wifi(accessPoint=UserAP)
    net.setPropagationModel(model="logDistance", exp=5)  # Higher path loss
    ap1 = net.addAccessPoint('ap1', ssid='ssid', mode='g', channel='1', position='10,30,0', txpower=20)
    ap2 = net.addAccessPoint('ap2', ssid='ssid', mode='g', channel='6', position='50,30,0', txpower=20)
    sta1 = net.addStation('sta1', position='12,30,0')
    c1 = net.addController('c1')
    net.configureWifiNodes()
    net.build(); c1.start(); ap1.start([c1]); ap2.start([c1])
    time.sleep(5)
    ap2_mac = ap2.intf('ap2-wlan1').mac
    log = []
    log.append((time.time(), 'Initial BSSID: %s' % get_bssid(sta1)))
    handover_time = None
    for tx in [10, 5, 2, 1, 0]:
        ap1.cmd('iw dev ap1-wlan1 set txpower fixed %d' % (tx*100))
        time.sleep(3)
        bssid = get_bssid(sta1)
        log.append((time.time(), 'AP1 txpower %d dBm, sta1 BSSID: %s' % (tx, bssid)))
        if bssid and bssid.lower() == ap2_mac.lower():
            handover_time = log[-1][0]
            log.append((handover_time, 'Handover to AP2 detected!'))
            break
    # If not handed over, move station closer to AP2
    if not handover_time:
        sta1.setPosition('48,30,0')
        time.sleep(5)
        bssid = get_bssid(sta1)
        log.append((time.time(), 'Moved sta1 near AP2, BSSID: %s' % bssid))
        if bssid and bssid.lower() == ap2_mac.lower():
            handover_time = log[-1][0]
            log.append((handover_time, 'Handover to AP2 detected after movement!'))
    print('\n=== Handover Log ===')
    for t, msg in log:
        print('%s: %s' % (time.strftime('%H:%M:%S', time.localtime(t)), msg))
    if handover_time:
        print('\nHandover time: %.3f seconds' % (handover_time - log[0][0]))
    else:
        print('\nHandover did not occur.')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology()

