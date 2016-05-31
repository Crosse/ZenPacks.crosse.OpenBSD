import re
from Products.DataCollector.plugins.CollectorPlugin import (
        SnmpPlugin, GetTableMap, GetMap,
        )


class PacketFilterTable(SnmpPlugin):
    relname = 'packetFilterTables'
    modname = 'ZenPacks.crosse.OpenBSD.PacketFilterTable'

    deviceProperties = SnmpPlugin.deviceProperties + (
            'zPfTableMonitorIgnore',
            'zPfIgnoreTables',
            )

    snmpGetTableMaps = (
            GetTableMap(
                'pfTblTable', '1.3.6.1.4.1.30155.1.9.128.1', {
                    '.2': 'pfTblName',
                    '.3': 'pfTblAddresses',
                    '.4': 'pfTblAnchorRefs',
                    '.5': 'pfTblRuleRefs',
                    }
                ),
            )


    def condition(self, device, log):
        shouldIgnore = getattr(device, 'zPfTableMonitorIgnore', False)
        if shouldIgnore:
            log.info('Modeler %s not modeling PF tables for device %s (zPfTableMonitorIgnore is true)',
                    self.name(), device.id)
        return not shouldIgnore


    def process(self, device, results, log):
        log.info('Modeler %s processing data for device %s',
                self.name(), device.id)

        rm = self.relMap()
        for snmpindex, row in results[1].get('pfTblTable', {}).items():
            name = row.get('pfTblName')
            if not name:
                log.warn('Skipping PF table with no name')
                continue

            # If the admin says we should ignore a table, ignore it.
            regex = getattr(device, 'zPfIgnoreTables', None)
            if regex and re.match(regex, name):
                log.info('Skipping %s (PF table) as it matches zPfIgnoreTables.', name)
                continue

            values = {}
            for key in row.keys():
                values[key] = row.get(key)

            values['id'] = self.prepId(name)
            values['title'] = name
            values['snmpindex'] = snmpindex.strip('.')
            del values['pfTblName']

            rm.append(self.objectMap(values))

        return rm
