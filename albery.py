



import os
p = os.getcwd()
for i in os.listdir(os.getcwd()):
    p2 = os.path.join(p,i)
    if os.path.isdir(p2) and '.git' not in p2:
        _command = f'touch {p2}/{i}_DEPLOYER'
        os.system(_command)