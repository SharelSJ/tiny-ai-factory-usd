from pxr import Usd

stage = Usd.Stage.Open(
    "payload_facility.usda",
    load=Usd.Stage.LoadAll
)

stage.Export("payload_facility_flattened.usda")