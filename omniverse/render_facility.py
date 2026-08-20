import sys
import tempfile
from pathlib import Path

import numpy as np
import ovrtx
import ovstage
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parent.parent
USD_PATH = REPO_ROOT / "payload_facility_flattened.usda"
OUTPUT_PATH = Path(__file__).resolve().parent / "output" / "facility.png"
RENDER_PRODUCT = "/Render/Camera"


def main():
    if not USD_PATH.is_file():
        raise FileNotFoundError(f"Facility USD not found: {USD_PATH}")

    # Keep the generated camera and render configuration separate from the
    # source asset. Forward slashes make the absolute path a valid USD asset
    # path on Windows.
    scene_usda = f'''#usda 1.0
(
    metersPerUnit = 1
    subLayers = [@{USD_PATH.as_posix()}@]
    upAxis = "Z"
)

over Xform "World"
{{
    def Camera "Camera"
    {{
        float focalLength = 35
        float horizontalAperture = 36
        matrix4d xformOp:transform = (
            (0.819232, 0.573462, 0, 0),
            (-0.261662, 0.373803, 0.889890, 0),
            (0.510260, -0.728943, 0.456863, 0),
            (9, -10, 7, 1)
        )
        uniform token[] xformOpOrder = ["xformOp:transform"]
    }}

    def DomeLight "EnvironmentLight"
    {{
        float inputs:intensity = 1200
    }}
}}

def Scope "Render"
{{
    def RenderProduct "Camera"
    {{
        rel camera = </World/Camera>
        int2 resolution = (1280, 720)
        token omni:rtx:rendermode = "RealTimePathTracing"
        rel orderedVars = <LdrColor>

        def RenderVar "LdrColor"
        {{
            string sourceName = "LdrColor"
        }}
    }}
}}
'''

    wrapper_path = None
    renderer = None
    stage = None
    try:
        with tempfile.NamedTemporaryFile(
            suffix=".usda", mode="w", encoding="utf-8", delete=False
        ) as wrapper:
            wrapper.write(scene_usda)
            wrapper_path = Path(wrapper.name)

        print("Creating renderer. The first run may compile shaders...", file=sys.stderr)
        renderer = ovrtx.Renderer()
        stage = ovstage.Stage("tiny-ai-factory.render-facility")
        renderer.attach_ovstage(stage)

        ordinal = 1
        print(f"Opening {USD_PATH}...", file=sys.stderr)
        ovstage.population.open_usd(stage, str(wrapper_path), ordinal=ordinal)
        stage.advance_write_floor(ordinal, ovstage.Scope.ALL).wait()

        print("Rendering one RGB frame...", file=sys.stderr)
        products = renderer.step(
            render_products={RENDER_PRODUCT},
            delta_time=1.0 / 60,
            ordinal=ordinal,
        )

        saved = False
        for product in products.values():
            for frame in product.frames:
                var = frame.render_vars["LdrColor"].map(device=ovrtx.Device.CPU)
                view = np.from_dlpack(var)
                pixels = view.copy()
                del view
                var.unmap()
                del var

                OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
                Image.fromarray(pixels[..., :3], mode="RGB").save(OUTPUT_PATH)
                saved = True
                break
            if saved:
                break

        if not saved:
            raise RuntimeError("The renderer returned no RGB frame")
        print(f"Saved to {OUTPUT_PATH}", file=sys.stderr)

        del frame, product, products
    finally:
        if renderer is not None and stage is not None:
            renderer.detach_ovstage()
        if stage is not None:
            stage.destroy()
        if renderer is not None:
            renderer.destroy()
        if wrapper_path is not None:
            wrapper_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
