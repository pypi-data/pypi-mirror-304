# SPDX-FileCopyrightText: Copyright (c) 2024 Scott Shawcroft for Adafruit Industries
#
# SPDX-License-Identifier: MIT

from abc import ABC

from circuitmatter.clusters.system_model import binding, descriptor, user_label


class SimpleDevice(ABC):
    def __init__(self, name):
        self.name = name
        self.servers = []
        self.descriptor = descriptor.DescriptorCluster()
        device_types = []
        for superclass in type(self).__mro__:
            if not hasattr(superclass, "DEVICE_TYPE_ID"):
                continue
            device_type = descriptor.DescriptorCluster.DeviceTypeStruct()
            device_type.DeviceType = superclass.DEVICE_TYPE_ID
            device_type.Revision = superclass.REVISION
            device_types.append(device_type)
        self.descriptor.DeviceTypeList = device_types
        self.descriptor.PartsList = []
        self.descriptor.ServerList = []
        self.descriptor.ClientList = []
        self.servers.append(self.descriptor)

        self.binding = binding.BindingCluster()
        self.servers.append(self.binding)

        self.user_label = user_label.UserLabelCluster()
        self.servers.append(self.user_label)

    def restore(self, nonvolatile):
        """Restore device state from the nonvolatile dictionary and hang onto it for any updates."""
        self.nonvolatile = nonvolatile
        for server in self.servers:
            cluster_hex = hex(server.CLUSTER_ID)
            if cluster_hex not in nonvolatile:
                nonvolatile[cluster_hex] = {}
            server.restore(nonvolatile[cluster_hex])
