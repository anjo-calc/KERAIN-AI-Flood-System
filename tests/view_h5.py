import h5py

f = h5py.File("kerain_satellite_model.h5", "r")
print(list(f.keys()))
