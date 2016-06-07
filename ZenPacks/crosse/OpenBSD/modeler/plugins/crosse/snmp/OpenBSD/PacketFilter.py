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
                '.1.3.6.1.4.1.30155.1.3.1.0': 'pfStateCount',
                '.1.3.6.1.4.1.30155.1.4.1.0': 'pfLogIfName',
                })
            )

    def process(self, device, results, log):
        log.info('Modeler %s processing data for device %s',
                self.name(), device.id)

        values = {}
        for key in results[0].keys():
            values[key] = results[0].get(key)

        values['id'] = self.prepId('pf')
        values['title'] = 'Packet Filter'
        values['pfRunning'] = True if (values['pfRunning'] == 1) else False

        rm = self.relMap()
        rm.append(self.objectMap(values))

        return rm
