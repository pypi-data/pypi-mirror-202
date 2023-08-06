# loxprox

*Experimental*: Proxies Loxone UDP data frames containing "Lumitech DMX" information to Philips Hue.

More input types will be added in the future to include additional data like readings from the Energy Meter.

## Docker

'''
docker run -d \
  --name loxprox_container \
  -p 12345:12345/udp \
  -v /path/to/host/config:/opt/nivos/loxprox/config \
  -v /path/to/host/logs:/opt/nivos/loxprox/log \
  -v /path/to/host/loxprox-supervisor.ini:/opt/nivos/loxprox/loxprox-supervisor.ini \
  loxprox_image
'''