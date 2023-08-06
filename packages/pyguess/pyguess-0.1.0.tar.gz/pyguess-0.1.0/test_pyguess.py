import pyguess

candidate = pyguess.find_street(0.5, "Rigistrasse 10", "Pfäffikon ZG")
print(candidate.street)
print(candidate.location)
