from ...device import Device


class Host:
    CONNECT_RESULT_PATTERN = "(connected to|already connected)"

    OFFLINE = "offline"
    DEVICE = "device"
    BOOTLOADER = "bootloader"

    async def _execute_cmd(self, cmd):
        async with await self.create_connection() as conn:
            await conn.send(cmd)
            return await conn.receive()

    async def devices(self):
        cmd = "host:devices"
        result = await self._execute_cmd(cmd)

        devices = []

        for line in result.split('\n'):
            if not line:
                break

            devices.append(Device(self, line.split()[0]))

        return devices
