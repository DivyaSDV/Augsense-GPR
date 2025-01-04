import os


directory = "/content/Interns/Input_files"
os.makedirs(directory, exist_ok=True)

# GPRMAX input file template
template = """
#title: B-scan from a metal cylinder buried in a dielectric half-space
#domain: 1.00 0.35 0.002
#dx_dy_dz: 0.002 0.002 0.002
#time_window: 6e-9
#material: 6 0.01 1 0 half_space
#waveform: ricker 1 1.5e9 my_ricker
#hertzian_dipole: z 0.260 0.25 0 my_ricker
#rx: 0.3 0.25 0
#src_steps: 0.002 0 0
#rx_steps: 0.002 0 0
#box: 0 0 0 1.00 0.25 0.002 half_space
#cylinder: 0.50 {height:0.3f} 0 0.50 {height:0.3f} 0.002 {radius} pec
"""

rad = [0.003,0.004,0.005,0.006,0.008,0.009,0.010,0.011,0.012]
for i in range(len(rad)):
  radius = rad[i]
  diameter = format(int(radius*1000)*2)

  height = 0.05
  for i in range(101):
    depth = format(250-int(height*1000))
    filename = os.path.join(directory, f"{diameter}mm_dia_{depth}mm_depth.in")
    with open(filename, 'w') as f:
        f.write(template.format(radius=radius,height = height))

    height+=0.001
  radius+= 0.001
    
    