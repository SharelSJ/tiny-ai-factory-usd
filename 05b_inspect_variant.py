# before:
# different configuration → duplicate asset/file

# with variants:
# one asset → named configuration choices

# variant set = dimension of choice
# variant = one choice
# variant selection = which choice currently contributes
# variant edit context = where I author the opinions belonging to that choice

# We can make Rack_01 use 72_GPU and 
# Rack_02 use 144_GPU 
# while both still reference the same rack.usda.

from pxr import Usd

stage = Usd.Stage.Open("rack_configurable.usda")

rack = stage.GetPrimAtPath("/Rack")
config = rack.GetVariantSet("configuration")

print("Current:", config.GetVariantSelection())
print("GPU Count:", rack.GetAttribute("gpuCount").Get())

config.SetVariantSelection("144_GPU")

print("Current:", config.GetVariantSelection())
print("GPU Count:", rack.GetAttribute("gpuCount").Get())