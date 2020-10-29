.DEFAULT_GOAL := help


### QUICK
# ¯¯¯¯¯¯¯

start: server.start ## Start

stop: server.stop ## Stop

restart: server.restart ## restart

remove: server.remove ## Stop server and remove volumes

logs: server.logs  ## Display server logs

include attachments/makefiles/server.mk

include attachments/makefiles/help.mk

