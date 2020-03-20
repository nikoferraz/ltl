import ltl

shipments = [16000, 42000, 8000, 12000, 38000, 1200, 1000, 18000, 28000, 7500, 17000, 37000]
trucks = [44000, 42000, 20000, 24000]
optimal_distribution = ltl.distribute_shipments(trucks, shipments)
print(optimal_distribution)