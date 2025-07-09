# vlan_checker.py
vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("Es una VLAN del rango normal.")
elif 1006 <= vlan <= 4094:
    print("Es una VLAN del rango extendido.")
else:
    print("Número de VLAN fuera de rango.")
