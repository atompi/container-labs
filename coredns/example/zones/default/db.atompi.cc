$TTL 3600
$ORIGIN atompi.cc.

@ IN SOA ns.atompi.cc. nsadmin.atompi.cc. (
    2025011617 ; Serial
    1H         ; Refresh
    600        ; Retry
    7D         ; Expire
    600        ; Negative Cache TTL
)

@ IN NS ns

ns IN A 192.168.1.2

; Custome
@                 IN A     192.168.220.128
*                 IN CNAME @
files             IN A     192.168.1.60
files             IN A     192.168.1.61
