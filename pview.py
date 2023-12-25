# A paraview script to load openfoam data and save the output data as csv at a plane.
# Run this script by creating a view.foam file in OpenFOAM case directory and run paraview by "pvpython pview.py". The script will output all quantities in CSV file.

from paraview.simple import *

viewfoam = OpenFOAMReader(FileName='view.foam')
viewfoam.UpdatePipeline()
clipFilter = Clip(registrationName='Clip1', Input=viewfoam)
clipFilter.ClipType = 'Box'
clipFilter.ClipType.Position = [-0.6, -0.3, -0.1]
clipFilter.ClipType.Length = [1.2, 0.6, 0.25]
sliceFilter = Slice(registrationName='sliceFilter', Input=clipFilter)
sliceFilter.SliceType = 'Plane'
sliceFilter.SliceType.Origin = [0.0, 0.0, 0.0]
sliceFilter.SliceType.Normal = [0.0, 1.0, 0.0]
animationScene = GetAnimationScene()

for index, timeStep in enumerate(animationScene.TimeKeeper.TimestepValues):
    animationScene.AnimationTime = timeStep
    UpdatePipeline(timeStep, sliceFilter)
    filename = f'sliced_data_timestep_{index}.csv'
    SaveData(filename, proxy=sliceFilter)
