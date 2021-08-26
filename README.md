# cisco_wlc_api

A Python library that provides an interface to the reverse-engineered API of the Cisco Wireless LAN Controller firmware

## Synopsys

At some point, Cisco released a firmware for the Cisco 2504 Wireless LAN Controller which included a new, simpler and
nicer-looking web interface. Although it exposes much less functionality than the previous (which is now an 'advanced'
interface), it uses a private API for getting data from the controller.
This is a marked improvement over the 'advanced' interface, for which all data is populated server-side. As a result,
"screen-scraping"/HTML parsing is required to get information, and it's very janky. Further, I found that doing this
would slowly result in a memory leak. As my WLC is ex-corporate and out of support, I couldn't exactly open a SmartNet
ticket :)

Through web request monitoring and some firmware analysis, I have determined most(?) of the API endpoints in use, and
how they are called. This Python module implements much of the API in a simple easy-to-use way.

## Requirements

* a Cisco Wireless LAN controller
* HTTP or HTTPS web interface enabled
* valid credentials
* recent(ish) firmware (7.5.* may be too old but 8.* is fine)
* Python 3.8 or newer