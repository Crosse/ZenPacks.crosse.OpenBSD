from Products.DataCollector.plugins.CollectorPlugin import (
        SnmpPlugin, GetTableMap, GetMap,
        )


class PacketFilter(SnmpPlugin):
    relname = 'packetFilters'
    modname = 'ZenPacks.crosse.OpenBSD.PacketFilter'

    snmpGetMap = (
            GetMap({
                '.1.3.6.1.4.1.30155.1.1.1.0': 'pfRunning',
                '.1.3.6.1.4.1.30155.1.1.2.0': 'pfRuntime',
                '.1.3.6.1.4.1.30155.1.1.3.0': 'pfDebug',
                '.1.3.6.1.4.1.30155.1.1.4.0': 'pfHostId',
                '.1.3.6.1.4.1.30155.1.2.1.0': 'pfCntMatch',
                '.1.3.6.1.4.1.30155.1.2.2.0': 'pfCntBadOffset',
                '.1.3.6.1.4.1.30155.1.2.3.0': 'pfCntFragment',
                '.1.3.6.1.4.1.30155.1.2.4.0': 'pfCntShort',
                '.1.3.6.1.4.1.30155.1.2.5.0': 'pfCntNormalize',
                '.1.3.6.1.4.1.30155.1.2.6.0': 'pfCntMemory',
                '.1.3.6.1.4.1.30155.1.2.7.0': 'pfCntTimestamp',
                '.1.3.6.1.4.1.30155.1.2.8.0': 'pfCntCongestion',
                '.1.3.6.1.4.1.30155.1.2.9.0': 'pfCntIpOption',
                '.1.3.6.1.4.1.30155.1.2.10.0': 'pfCntProtoCksum',
                '.1.3.6.1.4.1.30155.1.2.11.0': 'pfCntStateMismatch',
                '.1.3.6.1.4.1.30155.1.2.12.0': 'pfCntStateInsert',
                '.1.3.6.1.4.1.30155.1.2.13.0': 'pfCntStateLimit',
                '.1.3.6.1.4.1.30155.1.2.14.0': 'pfCntSrcLimit',
                '.1.3.6.1.4.1.30155.1.2.15.0': 'pfCntSynproxy',
                '.1.3.6.1.4.1.30155.1.2.16.0': 'pfCntTranslate',
                '.1.3.6.1.4.1.30155.1.2.17.0': 'pfCntNoRoute',
                '.1.3.6.1.4.1.30155.1.3.1.0': 'pfStateCount',
                '.1.3.6.1.4.1.30155.1.3.2.0': 'pfStateSearches',
                '.1.3.6.1.4.1.30155.1.3.3.0': 'pfStateInserts',
                '.1.3.6.1.4.1.30155.1.3.4.0': 'pfStateRemovals',
                })
            )

    def process(self, device, results, log):
        #import pdb; pdb.set_trace()

        values = {}
        for key in results[0].keys():
            values[key] = results[0].get(key)

        values['id'] = 'Packet Filter'
        values['pfRunning'] = True if (values['pfRunning'] == 1) else False

        rm = self.relMap()
        rm.append(self.objectMap(values))
        return rm
