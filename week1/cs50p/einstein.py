# Prompt the user for mass in kilograms
mass = int(input("m: "))

# Speed of light in meters per second
c = 300000000

# Calculate energy using E = mc^2
energy = mass * (c ** 2)

# Output the equivalent energy in Joules
print(energy)