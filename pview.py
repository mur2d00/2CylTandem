# A paraview script to import openfoam data and save dataPoints at probed planes
import paraview.simple as pvs
import numpy as np

# Load OpenFOAM data
viewfoam = pvs.OpenFOAMReader(FileName='view.foam')
viewfoam.UpdatePipeline()
calculator = pvs.Calculator(Input=viewfoam)
# calculate velocity of sediment and solid phase
calculator.ResultArrayName = 'Ua'
calculator.Function = '"alpha.a"*"U.a"'
calculator.UpdatePipeline()
calculator2 = pvs.Calculator(Input=calculator)
calculator2.ResultArrayName = 'Ub'
calculator2.Function = '"alpha.b"*"U.b"'
calculator2.UpdatePipeline()
# calculate the gradient of velocity vectors
gradient1 = pvs.Gradient(Input=calculator2)
gradient1.ScalarArray = ['POINTS', 'Ua',]
gradient1.UpdatePipeline()
gradient2 = pvs.Gradient(Input=gradient1)
gradient2.ScalarArray = ['POINTS', 'Ub']
gradient2.UpdatePipeline()
# calculate s of sediment phase
gradS1 = pvs.inputs[0].PointData['gradient1']
S_sediment = (gradS1 + np.transpose(gradS1)) / 2
pvs.output.PointData.append(S_sediment, 'Ss')
# calculate S of fluid phase
gradS2 = pvs.inputs[0].PointData['gradient2']
S_fluid = (gradS2 + np.transpose(gradS2)) / 2
pvs.output.PointData.append(S_fluid, 'Sf')
# create a box around 2 cylinders
clipFilter = pvs.Clip(registrationName='Clip1', Input=gradient2)
clipFilter.ClipType = 'Box'
clipFilter.ClipType.Position = [-0.6, -0.3, -0.1]
clipFilter.ClipType.Length = [1.2, 0.6, 0.25]
# create a slice normal to y-plane
sliceFilter = pvs.Slice(registrationName='sliceFilter', Input=clipFilter)
sliceFilter.SliceType = 'Plane'
sliceFilter.SliceType.Origin = [0.0, 0.0, 0.0]
sliceFilter.SliceType.Normal = [0.0, 1.0, 0.0]
animationScene = pvs.GetAnimationScene()

# Loop through each time step
for index, timeStep in enumerate(animationScene.TimeKeeper.TimestepValues):
    animationScene.AnimationTime = timeStep
    pvs.UpdatePipeline(timeStep, sliceFilter)
    filename = f'sliced_data_timestep_{index}.csv'
    pvs.SaveData(filename, proxy=sliceFilter)
