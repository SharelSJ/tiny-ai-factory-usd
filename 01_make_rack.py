from pxr import Usd, UsdGeom, UsdShade, Sdf, Gf


# ------------------------------------------------------------
# CREATE STAGE
# ------------------------------------------------------------

stage = Usd.Stage.CreateNew("rack.usda")

UsdGeom.SetStageMetersPerUnit(stage, 1.0)
UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)

rack = UsdGeom.Xform.Define(stage, "/Rack")
stage.SetDefaultPrim(rack.GetPrim())

# Machine-readable meaning
rack.GetPrim().CreateAttribute(
    "assetType",
    Sdf.ValueTypeNames.Token
).Set("computeRack")


# ------------------------------------------------------------
# ORGANIZATION
# ------------------------------------------------------------

UsdGeom.Scope.Define(stage, "/Rack/Geometry")
UsdGeom.Scope.Define(stage, "/Rack/Looks")


# ------------------------------------------------------------
# MATERIAL HELPER
# ------------------------------------------------------------

def make_material(name, color, metallic=0.0, roughness=0.4):
    """
    Creates a simple UsdPreviewSurface material.
    """

    material = UsdShade.Material.Define(
        stage,
        f"/Rack/Looks/{name}"
    )

    shader = UsdShade.Shader.Define(
        stage,
        f"/Rack/Looks/{name}/PreviewSurface"
    )

    shader.CreateIdAttr("UsdPreviewSurface")

    shader.CreateInput(
        "diffuseColor",
        Sdf.ValueTypeNames.Color3f
    ).Set(Gf.Vec3f(*color))

    shader.CreateInput(
        "metallic",
        Sdf.ValueTypeNames.Float
    ).Set(metallic)

    shader.CreateInput(
        "roughness",
        Sdf.ValueTypeNames.Float
    ).Set(roughness)

    material.CreateSurfaceOutput().ConnectToSource(
        shader.ConnectableAPI(),
        UsdShade.Tokens.surface
    )

    return material


# Dark metallic rack frame
frame_material = make_material(
    "Frame",
    (0.08, 0.10, 0.12),
    metallic=0.7,
    roughness=0.3
)

# Nearly black server equipment
server_material = make_material(
    "Server",
    (0.015, 0.02, 0.025),
    metallic=0.0,
    roughness=0.4
)

# Green status lights
accent_material = make_material(
    "Accent",
    (0.0, 0.8, 0.2),
    metallic=0.0,
    roughness=0.35
)


# ------------------------------------------------------------
# BOX HELPER
# ------------------------------------------------------------

def make_box(name, position, dimensions, material):
    """
    Create one rectangular box.

    position   = center of box (x, y, z), in meters
    dimensions = width, depth, height, in meters
    """

    cube = UsdGeom.Cube.Define(
        stage,
        f"/Rack/Geometry/{name}"
    )

    # Start with a 1 x 1 x 1 cube
    cube.GetSizeAttr().Set(1.0)

    xform = UsdGeom.XformCommonAPI(cube)

    xform.SetTranslate(
        Gf.Vec3d(*position)
    )

    xform.SetScale(
        Gf.Vec3f(*dimensions)
    )

    # Bind material
    UsdShade.MaterialBindingAPI.Apply(
        cube.GetPrim()
    ).Bind(material)

    return cube


# ------------------------------------------------------------
# RACK FRAME
#
# Overall dimensions:
# approximately 0.6m wide
# x 1.2m deep
# x 2.0m tall
# ------------------------------------------------------------

POST_WIDTH = 0.05
POST_DEPTH = 0.05
RACK_HEIGHT = 2.0

# Four vertical posts
make_box(
    "FrontLeftPost",
    (-0.275, -0.575, 1.0),
    (POST_WIDTH, POST_DEPTH, RACK_HEIGHT),
    frame_material
)

make_box(
    "FrontRightPost",
    (0.275, -0.575, 1.0),
    (POST_WIDTH, POST_DEPTH, RACK_HEIGHT),
    frame_material
)

make_box(
    "RearLeftPost",
    (-0.275, 0.575, 1.0),
    (POST_WIDTH, POST_DEPTH, RACK_HEIGHT),
    frame_material
)

make_box(
    "RearRightPost",
    (0.275, 0.575, 1.0),
    (POST_WIDTH, POST_DEPTH, RACK_HEIGHT),
    frame_material
)

# Bottom frame
make_box(
    "Base",
    (0.0, 0.0, 0.03),
    (0.6, 1.2, 0.06),
    frame_material
)

# Top frame
make_box(
    "Top",
    (0.0, 0.0, 1.97),
    (0.6, 1.2, 0.06),
    frame_material
)


# ------------------------------------------------------------
# SERVER UNITS
# ------------------------------------------------------------

SERVER_WIDTH = 0.52
SERVER_DEPTH = 1.05
SERVER_HEIGHT = 0.15

FIRST_SERVER_Z = 0.16
SERVER_SPACING = 0.20

for i in range(8):

    server_number = i + 1

    z = FIRST_SERVER_Z + i * SERVER_SPACING

    server = make_box(
        f"Server_{server_number:02d}",
        (0.0, 0.0, z),
        (
            SERVER_WIDTH,
            SERVER_DEPTH,
            SERVER_HEIGHT
        ),
        server_material
    )

    # Structured metadata on each server
    server.GetPrim().CreateAttribute(
        "slotIndex",
        Sdf.ValueTypeNames.Int
    ).Set(server_number)

    # Small green status indicator on front face
    make_box(
        f"Server_{server_number:02d}_Status",
        (0.20, -0.535, z),
        (0.035, 0.015, 0.025),
        accent_material
    )


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

stage.GetRootLayer().Save()

print("Created rack.usda")