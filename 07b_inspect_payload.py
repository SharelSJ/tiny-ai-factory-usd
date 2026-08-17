# working-set management
# open stage with no payloads loaded first
# reference = "compose this external asset here"
# payload = "compose this external content here, 
# but make it optional in my working set"

from pxr import Usd

# OpenUSD defaults to loading all payloads
# LoadNone to show deferred-loading behavior
stage = Usd.Stage.Open(
    "payload_facility.usda",
    load=Usd.Stage.LoadNone
)

datahall_b = stage.GetPrimAtPath(
    "/World/DataHall_B"
)

print("Before load:")
print("Loaded?", datahall_b.IsLoaded())

for child in datahall_b.GetChildren():
    print(child.GetPath())

#load
datahall_b.Load()

print("\nAfter load:")
print("Loaded?", datahall_b.IsLoaded())

for child in datahall_b.GetChildren():
    print(child.GetPath())

#unload
datahall_b.Unload()

print("\nAfter load:")
print("Loaded?", datahall_b.IsLoaded())
