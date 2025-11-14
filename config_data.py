config_data = [
    {
        "devicename": "DK-P1-SW01", 
        "devicetype": "cisco_ios", 
        "host": "10.1.99.11", 
    "config": """version 15.2
no service pad
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname DK-P1-SW01
!
boot-start-marker
boot-end-marker
!
logging userinfo
enable secret 5 $1$.Bet$zY/vKOvR4J81fT1r08LGk0
!
username admin secret 5 $1$aqIY$pTFQI3Uf1Kk32FYJWR6C1.
no aaa new-model
clock timezone utc 1 0
switch 1 provision ws-c2960x-24ps-l
!
!
no ip domain-lookup
ip domain-name DK-P1-SW01.funpark.local
!
!
!
!
!
!
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
spanning-tree pathcost method long
spanning-tree vlan 10,20,30,50,99,128 priority 61440
!
!
!
!
vlan internal allocation policy ascending
!
!
! 
!
!
!
!
!
!
!
!
interface Port-channel11
 switchport trunk allowed vlan 10,20,30,50,99,128
 switchport mode trunk
!
interface Port-channel21
 switchport trunk allowed vlan 10,20,30,50,99,128
 switchport mode trunk
!
interface FastEthernet0
 no ip address
 shutdown
!
interface GigabitEthernet1/0/1
 description Port channel to DK-P1-CRSW01
 switchport trunk allowed vlan 10,20,30,50,99,128
 switchport mode trunk
 channel-group 11 mode active
!
interface GigabitEthernet1/0/2
 description Port channel to DK-P1-CRSW01
 switchport trunk allowed vlan 10,20,30,50,99,128
 switchport mode trunk
 channel-group 11 mode active
!
interface GigabitEthernet1/0/3
 description Port channel to DK-P1-CRSW02
 switchport trunk allowed vlan 10,20,30,50,99,128
 switchport mode trunk
 channel-group 21 mode active
!
interface GigabitEthernet1/0/4
 description Port channel to DK-P1-CRSW02
 switchport trunk allowed vlan 10,20,30,50,99,128
 switchport mode trunk
 channel-group 21 mode active
!
interface GigabitEthernet1/0/5
 description Ap port
 switchport access vlan 99
 switchport trunk allowed vlan 10,99,128
 switchport mode trunk
!
interface GigabitEthernet1/0/6
 description Unused port in shutdown
 switchport mode access
 shutdown
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/7
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/8
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/9
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/10
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/11
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/12
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/13
 description Temp administration vlan access
 switchport access vlan 10
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/14
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/15
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/16
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/17
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/18
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/19
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/20
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/21
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/22
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/23
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/24
 description Unused port in shutdown
 switchport mode access
 spanning-tree portfast
 spanning-tree bpduguard enable
!
interface GigabitEthernet1/0/25
!
interface GigabitEthernet1/0/26
!
interface GigabitEthernet1/0/27
!
interface GigabitEthernet1/0/28
!
interface Vlan1
 no ip address
 shutdown
!
interface Vlan99
 ip address 10.1.99.11 255.255.255.0
!
ip default-gateway 10.1.99.1
ip http server
ip http secure-server
!
ip ssh version 2
!
logging facility local0
logging host 10.1.50.50
access-list 10 permit 10.1.99.0 0.0.0.255
!
!
!
line con 0
line vty 0 4
 access-class 10 in
 exec-timeout 480 0
 login local
 transport input ssh
line vty 5 15
 login
!
end
    """
        },
    {
        "devicename": "DK-P1-SW04", 
        "devicetype": "cisco_ios", 
        "host": "10.1.99.14", 
        "config": """ 
     end
     """},
    {
        "devicename": "DK-P2-SW01", 
        "devicetype": "cisco_ios", 
        "host": "10.2.99.11", 
        "config": """ 
     end
     """},
    {
        "devicename": "DK-P4-SW01", 
        "devicetype": "cisco_ios", 
        "host": "10.4.99.11", 
        "config": """ 
     end
     """},
    {
        "devicename": "DK-P1-CRSW01", 
        "devicetype": "cisco_ios", 
        "host": "10.1.99.2", 
        "config": """ """},
    {
        "devicename": "DK-P1-CRSW02", 
        "devicetype": "cisco_ios", 
        "host": "10.1.99.3", 
        "config": """ 
        end
        """},
    {
        "devicename": "DK-P2-CRSW01", 
        "devicetype": "cisco_ios", 
        "host": "10.2.99.2", 
        "config": """ 
        end
        """},
    {
        "devicename": "DK-P4-CRSW01", 
        "devicetype": "cisco_ios", 
        "host": "10.4.99.2", 
        "config": """ 
        end
        """}
]