import subprocess

scripts = [
    "01_make_rack.py",
    "02_make_facility.py",
    "03_make_datahall.py",
    "04a_make_rack_assets.py",
    "04b_make_cooling.py",
    "04c_make_operations.py",
    "04d_make_facility.py",
    "04e_inspection_facility.py",
    "05a_make_configurable_rack.py",
    "05b_inspect_variant.py",
    "05c_make_variant_facility.py",
    "05d_inspect_variant_facility.py",
    "06_make_datahall_b.py",
    "07a_make_payload_facility.py",
    "07b_inspect_payload.py",
    "08_add_semantics.py",
    "09_validate_facility.py",
    "10_export_flattened_view.py",
]

for script in scripts:
    print(f"\n=== Running {script} ===")
    subprocess.run(
        ["/usr/local/bin/python3", script],
        check=True
    )

print("\nBuild complete.")