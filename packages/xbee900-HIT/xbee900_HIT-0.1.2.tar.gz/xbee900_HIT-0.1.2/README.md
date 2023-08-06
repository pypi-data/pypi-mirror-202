# xbee900_HIT
## Installation
```python
python3 -m pip install xbee900_HIT
```
## Example
### send
```python
from xbee900_HIT import xbee
import logging
logging.basicConfig(filename='xbee.log',
                    format='%(asctime)s %(message)s', level=logging.INFO)


def send():
    device = xbee.Xbee('/dev/tty.usbserial-2', 9600)
    with open('3KB.txt', 'rb') as f:
        data = f.read()
        # broadcast
        device.send_packet(data)

    with open('1KB.txt', 'rb') as f:
        data = f.read()
        # point2point
        device.send_packet(data, remoteAddr="0013A20041BB7684")


send()

```

### receive

```python
from xbee900_HIT import xbee
import logging

logging.basicConfig(filename='xbee.log',
                    format='%(asctime)s %(message)s', level=logging.INFO)


def receive():
    device = xbee.Xbee('/dev/tty.usbserial-1', 230400)
    while True:
        data, remote = device.receive_packet()
        print(f'from {remote} :length of data:{len(data)},receive data: {data}')


receive()
```