from pxr import Usd

stage = Usd.Stage.Open("variant_facility.usda")

for path in [
    "/World/DataHall_A/Rack_01",
    "/World/DataHall_A/Rack_02",
]:
    rack = stage.GetPrimAtPath(path)

    config = rack.GetVariantSet("configuration")
    gpu_count = rack.GetAttribute("gpuCount").Get()

    print(
        path,
        config.GetVariantSelection(),
        gpu_count
    )