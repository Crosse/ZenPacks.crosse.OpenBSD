from Products.DataCollector.plugins.CollectorPlugin import (
        SnmpPlugin, GetTableMap, GetMap,
        )


class PacketFilterTable(SnmpPlugin):
    relname = 'packetFilterTables'
    modname = 'ZenPacks.crosse.OpenBSD.PacketFilterTable'

    deviceProperties = SnmpPlugin.deviceProperties + (
            'zPfIgnoreTables',
            )

    snmpGetTableMaps = (
            GetTableMap(
                'pfTblTable', '1.3.6.1.4.1.30155.1.9.128.1', {
                    '.1': 'pfTblIndex',
                    '.2': 'pfTblName',
                    '.3': 'pfTblAddresses',
                    '.4': 'pfTblAnchorRefs',
                    '.5': 'pfTblRuleRefs',
                    '.6': 'pfTblEvalsMatch',
                    '.7': 'pfTblEvalsNoMatch',
                    '.8': 'pfTblInPassPkts',
                    '.9': 'pfTblInPassBytes',
                    '.11': 'pfTblInBlockPkts',
                    '.11': 'pfTblInBlockBytes',
                    '.12': 'pfTblInXPassPkts',
                    '.13': 'pfTblInXPassBytes',
                    '.14': 'pfTblOutPassPkts',
                    '.15': 'pfTblOutPassBytes',
                    '.16': 'pfTblOutBlockPkts',
                    '.17': 'pfTblOutBlockBytes',
                    '.18': 'pfTblOutXPassPkts',
                    '.19': 'pfTblOutXPassBytes',
                    '.20': 'pfTblStatsCleared',
                    '.21': 'pfTblInMatchPkts',
                    '.22': 'pfTblInMatchBytes',
                    '.23': 'pfTblOutMatchPkts',
                    '.24': 'pfTblOutMatchBytes',
                    }
                ),
            )


    def condition(self, device, log):
        shouldIgnore = getattr(device, 'zPfIgnoreTables', False)
        if shouldIgnore:
            log.info('Modeler %s not modeling PF tables for device %s (zPfIgnoreTables is true)',
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

            values = {}
            for key in row.keys():
                values[key] = row.get(key)

            values['id'] = self.prepId(name)
            values['title'] = name
            values['snmpindex'] = snmpindex.strip('.')
            del values['pfTblName']

            rm.append(self.objectMap(values))

        return rm
