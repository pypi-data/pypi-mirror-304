import ctypes

# Load the dynamic library
lib = ctypes.CDLL('./iokitGPULib.dylib')

# Define the function return type as c_char_p (pointer to C char)
lib.getGPUInfo.restype = ctypes.c_char_p

# Call the function and get the result
gpu_info = lib.getGPUInfo()
print("Detected GPUs:", gpu_info)

