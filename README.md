# vortex_tracker
The helper app to prepare crop objects (area of interests) from NetCDF file is in directory crop_sample_app.
Run it as
```
python crop_sample_app.py
```

The app is tested on Linux system, and unfortunatly it has problem to run on Mac right now.

# Vortex tracking
Tracking vortex involves detecting vortices in each image frame and using Multiple hypothesis tracking (MHT) to connect each position detected into trajectories.
[detection](https://youtu.be/Y9RDsoVO0cU)
[tracking](https://youtu.be/xkx5Nel-cHY)
