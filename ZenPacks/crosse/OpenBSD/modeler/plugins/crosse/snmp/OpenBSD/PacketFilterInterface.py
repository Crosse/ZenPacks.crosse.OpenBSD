import re
from Products.DataCollector.plugins.CollectorPlugin import (
        SnmpPlugin, GetTableMap, GetMap,
        )

class PacketFilterInterface(SnmpPlugin):
    compname = 'packetFilter/pf'
    relname = 'packetFilterInterfaces'
    modname = 'ZenPacks.crosse.OpenBSD.PacketFilterInterface'

    deviceProperties = SnmpPlugin.deviceProperties + (
            'zPfInterfaceMonitorIgnore',
            'zPfIgnoreInterfaces',
            )

    snmpGetTableMaps = (
            GetTableMap(
                'pfIfTable', '1.3.6.1.4.1.30155.1.8.128.1', {
                    '.2':  'pfIfDescr',
                    '.3':  'pfIfType',
                    '.4':  'pfIfRefs',
                    '.5':  'pfIfRules',
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

            # If the admin says we should ignore an interface, ignore it.
            regex = getattr(device, 'zPfIgnoreInterfaces', None)
            if regex and re.match(regex, desc):
                log.info('Skipping %s (PF interface) as it matches zPfIgnoreInterfaces.', desc)
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
