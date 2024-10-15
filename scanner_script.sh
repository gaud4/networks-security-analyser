sudo tshark -i wlan0 -Y "http" -T fields -e ip.src -e ip.dst
```     
