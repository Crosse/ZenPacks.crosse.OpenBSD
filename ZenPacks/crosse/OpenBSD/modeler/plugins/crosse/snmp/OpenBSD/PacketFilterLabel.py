import re
from Products.DataCollector.plugins.CollectorPlugin import (
        SnmpPlugin, GetTableMap, GetMap,
        )


class PacketFilterLabel(SnmpPlugin):
    relname = 'packetFilterLabels'
    modname = 'ZenPacks.crosse.OpenBSD.PacketFilterLabel'

    deviceProperties = SnmpPlugin.deviceProperties + (
            'zPfLabelMonitorIgnore',
            'zPfIgnoreLabels',
            )

    snmpGetTableMaps = (
            GetTableMap(
                'pfLabelTable', '1.3.6.1.4.1.30155.1.10.128.1', {
                    '.2': 'pfLabelName',
                    '.3': 'pfLabelEvals',
                    '.4': 'pfLabelPkts',
                    '.5': 'pfLabelBytes',
                    '.10': 'pfLabelTotalStates',
                    }
                ),
            )


    def condition(self, device, log):
        shouldIgnore = getattr(device, 'zPfLabelMonitorIgnore', False)
        if shouldIgnore:
            log.info('Modeler %s not modeling PF labels for device %s (zPfLabelMonitorIgnore is true)',
                    self.name(), device.id)
        return not shouldIgnore


    def process(self, device, results, log):
        log.info('Modeler %s processing data for device %s',
                self.name(), device.id)

        rm = self.relMap()
        maps = {}
        for snmpindex, row in results[1].get('pfLabelTable', {}).items():
            name = row.get('pfLabelName')
            if not name:
                log.warn('Skipping PF label with no name')
                continue

            # If the admin says we should ignore a label, ignore it.
            regex = getattr(device, 'zPfIgnoreLabels', None)
            if regex and re.match(regex, name):
                log.info('Skipping %s (PF label) as it matches zPfIgnoreLabels.', name)
                continue

            # Aggregate same-named label statistics.
            values = maps.get(name, {})
            if len(values.keys()) == 0:
                log.debug('Creating a new map for %s', name)
            else:
                log.debug('Using existing map for %s', name)

            for key in row.keys():
                if key == 'pfLabelName':
                    continue
                value = row.get(key)
                values[key] = values.get(key, 0) + value

            values['id'] = self.prepId(name)
            values['title'] = name
            values['snmpindex'] = snmpindex.strip('.')
            maps[name] = values

        for name in maps:
            rm.append(self.objectMap(maps[name]))

        return rm
