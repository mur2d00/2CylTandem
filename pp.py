import numpy as np
import re
import matplotlib.pyplot as plt

# Open the file with the data
with open('alpha.a', 'r') as file:
    lines = file.readlines()
# Prepare a list to hold the extracted x, y, z, time, and the line after time
xData, yData, zData, alphaData, UaData, UbData, alphaEffData, muI, nuEffaData, nuEffbData, nuFraData, nutaData, nutbData, p_rbghData, paData, pffData  = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
start_reading = False
# Process each line
for line in lines:
    if line.startswith('# Probe'):
        # Extract the x, y, z values
        parts = line.split('(')[1].split(')')[0].split()
        x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
        xData.append(x)
        yData.append(y)
        zData.append(z)
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        alphaData.append(columns)
    if "Time" in line:
        start_reading = True  

xData1 = np.array(xData)
yData1 = np.array(yData)
zData1 = np.array(zData)
alphaData1 = np.array(alphaData)

# Reshape it to 2d array
xData2 = xData1.reshape(-1, 1)
yData2 = yData1.reshape(-1, 1)
zData2 = zData1.reshape(-1, 1)
alphaData2 = np.array(alphaData1.T)

# Final Data arrangement
result = np.concatenate((xData2, yData2,zData2), axis=1)
zeros_column = np.zeros((1000, 1))
result = np.hstack((result, zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column,zeros_column))
result3DTemp = np.repeat(result[:, :, np.newaxis], 72, axis=2)
alphaData2_3D = alphaData2[:, np.newaxis, :]
result3D = result3DTemp.copy()
result3D[:, 3, :] = alphaData2_3D[:, 0, :]
#print("Shape of the result array:", result3D.shape)
file.close()
del columns
del line
del lines

# Import U.a
with open('U.a', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        UaData.append(columns)
    if "Time" in line:
        start_reading = True  
UaData1 = np.array(UaData)
counter = 0
UaX = np.zeros((72, 1000))
for col in range(0, UaData1.shape[1], 3):
    UaX1 = UaData1[:, col]
    UaX1 = [element.lstrip('(') for element in UaX1]
    UaX1Temp = np.array(UaX1)
    UaX[:,counter] = UaX1Temp
    counter += 1
counter = 0
UaY= np.zeros((72, 1000))
for col2 in range(1, UaData1.shape[1], 3):
    UaY1 = UaData1[:, col2]
    UaY1Temp = np.array(UaY1)
    UaY[:,counter] = UaY1Temp
    counter += 1
counter = 0
UaZ= np.zeros((72, 1000))
for col3 in range(2, UaData1.shape[1], 3):
    UaZ1 = UaData1[:, col3]
    UaZ1 = [element.rstrip(')') for element in UaZ1]
    UaZ1Temp = np.array(UaZ1)
    UaZ[:,counter] = UaZ1Temp
    counter += 1
# Add Ua to Final Data
  
UaX_Temp = UaX.T
UaX_Temp_3D = UaX_Temp[:, np.newaxis, :]
result3D[:, 4, :] = UaX_Temp_3D[:, 0, :]

UaY_Temp = UaY.T
UaY_Temp_3D = UaY_Temp[:, np.newaxis, :]
result3D[:, 5, :] = UaY_Temp_3D[:, 0, :]

UaZ_Temp = UaZ.T
UaZ_Temp_3D = UaZ_Temp[:, np.newaxis, :]
result3D[:, 6, :] = UaZ_Temp_3D[:, 0, :]
file.close()
del columns
del line
del lines
# Import U.a
with open('U.b', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        UbData.append(columns)
    if "Time" in line:
        start_reading = True  
UbData1 = np.array(UbData)
counter = 0
UbX = np.zeros((72, 1000))
for col in range(0, UaData1.shape[1], 3):
    UbX1 = UaData1[:, col]
    UbX1 = [element.lstrip('(') for element in UaX1]
    UbX1Temp = np.array(UbX1)
    UbX[:,counter] = UbX1Temp
    counter += 1
counter = 0
UbY= np.zeros((72, 1000))
for col2 in range(1, UbData1.shape[1], 3):
    UbY1 = UbData1[:, col2]
    UbY1Temp = np.array(UbY1)
    UbY[:,counter] = UbY1Temp
    counter += 1
counter = 0
UbZ= np.zeros((72, 1000))
for col3 in range(2, UbData1.shape[1], 3):
    UbZ1 = UbData1[:, col3]
    UbZ1 = [element.rstrip(')') for element in UbZ1]
    UbZ1Temp = np.array(UbZ1)
    UbZ[:,counter] = UbZ1Temp
    counter += 1
# Add Ua to Final Data
  
UbX_Temp = UbX.T
UbX_Temp_3D = UbX_Temp[:, np.newaxis, :]
result3D[:, 7, :] = UbX_Temp_3D[:, 0, :]

UbY_Temp = UbY.T
UbY_Temp_3D = UbY_Temp[:, np.newaxis, :]
result3D[:, 8, :] = UbY_Temp_3D[:, 0, :]

UbZ_Temp = UbZ.T
UbZ_Temp_3D = UbZ_Temp[:, np.newaxis, :]
result3D[:, 9, :] = UbZ_Temp_3D[:, 0, :]
file.close()

del columns
del line
del lines    
with open('alphaEff.a', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        alphaEffData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
alphaEffData1 = np.array(alphaEffData)
alphaEffData2 = np.array(alphaEffData1.T)
alphaEffData2_3D = alphaEffData2[:, np.newaxis, :]
result3D[:, 10, :] = alphaEffData2_3D[:, 0, :]



del columns
del line
del lines    
with open('muI', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        muI.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
muI1 = np.array(muI)
muI2 = np.array(muI1.T)
muI2_3D = muI2[:, np.newaxis, :]
result3D[:, 11, :] = muI2_3D[:, 0, :]


del columns
del line
del lines    
with open('nuEffa', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        nuEffaData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
nuEffaData1 = np.array(nuEffaData)
nuEffaData2 = np.array(nuEffaData1.T)
nuEffaData2_3D = nuEffaData2[:, np.newaxis, :]
result3D[:, 12, :] = nuEffaData2_3D[:, 0, :]

del columns
del line
del lines    
with open('nuEffb', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        nuEffbData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
nuEffbData1 = np.array(nuEffbData)
nuEffbData2 = np.array(nuEffbData1.T)
nuEffbData2_3D = nuEffbData2[:, np.newaxis, :]
result3D[:, 13, :] = nuEffbData2_3D[:, 0, :]

del columns
del line
del lines    
with open('nut.a', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        nutaData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
nutaData1 = np.array(nutaData)
nutaData2 = np.array(nutaData1.T)
nutaData2_3D = nutaData2[:, np.newaxis, :]
result3D[:, 14, :] = nutaData2_3D[:, 0, :]

del columns
del line
del lines    
with open('nut.b', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        nutbData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
nutbData1 = np.array(nutbData)
nutbData2 = np.array(nutbData1.T)
nutbData2_3D = nutbData2[:, np.newaxis, :]
result3D[:, 15, :] = nutbData2_3D[:, 0, :]

del columns
del line
del lines    
with open('nuFra', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        nuFraData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
nuFraData1 = np.array(nuFraData)
nuFraData2 = np.array(nuFraData1.T)
nuFraData2_3D = nuFraData2[:, np.newaxis, :]
result3D[:, 16, :] = nuFraData2_3D[:, 0, :]


del columns
del line
del lines    
with open('p_rbgh', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        p_rbghData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
p_rbghData1 = np.array(p_rbghData)
p_rbghData2 = np.array(p_rbghData1.T)
p_rbghData2_3D = p_rbghData2[:, np.newaxis, :]
result3D[:, 17, :] = p_rbghData2_3D[:, 0, :]

del columns
del line
del lines    
with open('pa', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        paData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
paData1 = np.array(paData)
paData2 = np.array(paData1.T)
paData2_3D = paData2[:, np.newaxis, :]
result3D[:, 18, :] = paData2_3D[:, 0, :]

del columns
del line
del lines    
with open('pff', 'r') as file:
    lines = file.readlines()
start_reading = False
for line in lines:
    if start_reading:
        # Split the line into columns and ignore the first column
        columns = line.strip().split()[1:]
        pffData.append(columns)
    if "Time" in line:
        start_reading = True
#print(alphaEffData)        
pffData1 = np.array(pffData)
pffData2 = np.array(pffData1.T)
pffData2_3D = pffData2[:, np.newaxis, :]
result3D[:, 19, :] = pffData2_3D[:, 0, :]


print("result 3D array has the following format: X, Y, Z, alpha.a, UaX, UaY, UaZ, UbX, UbY, UbZ, alphaEff, muI, nuEffa, nuEffb, nut.a, nut.b, nuFra, p_rbghData,pa, pff ")
print("Dimensions of 3D Results (probes points x attributes, timesteps):", result3D.shape)


plt.figure(figsize=(4, 9))
plt.plot(result3D[:,3,70], result3D[:,2,70])
plt.xlabel("volumetric sediment concentration")
plt.ylabel("depth")
plt.grid(True)
plt.savefig('UaX.png', facecolor="w", edgecolor="w", format="png", dpi=500)
