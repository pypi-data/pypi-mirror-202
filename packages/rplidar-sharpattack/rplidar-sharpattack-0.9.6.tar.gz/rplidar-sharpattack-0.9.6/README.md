# RPLidar 

Simple and lightweight Python module for working with RPLidar rangefinder scanners. Forked from [Roboticia/RPLidar](https://github.com/Roboticia/RPLidar), originally to fix a specific bug. Aims for Python 3 compatibility only.

For protocol specifications please refer to the slamtec
[document](http://www.slamtec.com/download/lidar/documents/en-us/rplidar_interface_protocol_en.pdf).


## Documentation

View the latest rplidar documentation at http://rplidar.rtfd.org/.


## Usage example

Simple example:
```Python
from rplidar import RPLidar
lidar = RPLidar('/dev/ttyUSB0')

info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

for i, scan in enumerate(lidar.iter_scans()):
    print('%d: Got %d measurments' % (i, len(scan)))
    if i > 10:
        break

lidar.stop()
lidar.stop_motor()
lidar.disconnect()
```
