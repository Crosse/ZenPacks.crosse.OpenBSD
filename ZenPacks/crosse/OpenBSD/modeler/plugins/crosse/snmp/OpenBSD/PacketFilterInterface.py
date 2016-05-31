from Products.DataCollector.plugins.CollectorPlugin import (
        SnmpPlugin, GetTableMap, GetMap,
        )


class PacketFilterInterface(SnmpPlugin):
    relname = 'packetFilterInterfaces'
    modname = 'ZenPacks.crosse.OpenBSD.PacketFilterInterface'

    deviceProperties = SnmpPlugin.deviceProperties + (
            'zPfInterfaceMonitorIgnore',
            )

    snmpGetTableMaps = (
            GetTableMap(
                'pfIfTable', '1.3.6.1.4.1.30155.1.8.128.1', {
                    '.1':  'pfIfIndex',
                    '.2':  'pfIfDescr',
                    '.3':  'pfIfType',
                    '.4':  'pfIfRefs',
                    '.5':  'pfIfRules',
                    '.6':  'pfIfIn4PassPkts',
                    '.7':  'pfIfIn4PassBytes',
                    '.8':  'pfIfIn4BlockPkts',
                    '.9':  'pfIfIn4BlockBytes',
                    '.10': 'pfIfOut4PassPkts',
                    '.11': 'pfIfOut4PassBytes',
                    '.12': 'pfIfOut4BlockPkts',
                    '.13': 'pfIfOut4BlockBytes',
                    '.14':  'pfIfIn6PassPkts',
                    '.15':  'pfIfIn6PassBytes',
                    '.16':  'pfIfIn6BlockPkts',
                    '.17':  'pfIfIn6BlockBytes',
                    '.18':  'pfIfOut6PassPkts',
                    '.19':  'pfIfOut6PassBytes',
                    '.20':  'pfIfOut6BlockPkts',
                    '.21':  'pfIfOut6BlockBytes',
                    }
                ),
            )

    def condition(self, device, log):
        shouldIgnore = getattr(device, 'zPfInterfaceMonitorIgnore', False)
        if shouldIgnore:
            log.info('Modeler %s not modeling PF interfaces for device %s (zPfInterfaceMonitorIgnore is true)',
                    self.name(), device.id)
        return not shouldIgnore


    def process(self, device, results, log):
        log.info('Modeler %s processing data for device %s',
                self.name(), device.id)

        rm = self.relMap()
        for snmpindex, row in results[1].get('pfIfTable', {}).items():
            desc = row.get('pfIfDescr')
            if not desc:
                log.warn('Skipping PF interface with no description')
                continue

            values = {}
            for key in row.keys():
                values[key] = row.get(key)

            values['id'] = self.prepId(desc)
            values['title'] = desc
            values['snmpindex'] = snmpindex.strip('.')
            del values['pfIfDescr']

            rm.append(self.objectMap(values))

        return rm
