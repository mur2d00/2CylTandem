# A paraview script to load openfoam data and save the output data as csv at a plane.
from paraview.simple import *

# Load OpenFOAM data
viewfoam = OpenFOAMReader(FileName='view.foam')

# Update to ensure data is loaded
viewfoam.UpdatePipeline()

# Create a clip & a slice filter
clipFilter = Clip(registrationName='Clip1', Input=viewfoam)
clipFilter.ClipType = 'Box'
clipFilter.ClipType.Position = [-0.6, -0.3, -0.1]
clipFilter.ClipType.Length = [1.2, 0.6, 0.25]
sliceFilter = Slice(registrationName='sliceFilter', Input=clipFilter)
sliceFilter.SliceType = 'Plane'
sliceFilter.SliceType.Origin = [0.0, 0.0, 0.0]
sliceFilter.SliceType.Normal = [0.0, 1.0, 0.0]
# Get the animation scene
animationScene = GetAnimationScene()

# Loop through each time step
for index, timeStep in enumerate(animationScene.TimeKeeper.TimestepValues):
    # Update the time step
    animationScene.AnimationTime = timeStep
    
    # Update the pipeline for the new time step
    UpdatePipeline(timeStep, sliceFilter)

    # Define the output filename for each time step
    filename = f'sliced_data_timestep_{index}.csv'

    # Export the sliced data to a CSV file
    SaveData(filename, proxy=sliceFilter)
