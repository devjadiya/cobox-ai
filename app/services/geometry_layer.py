import random

GEOMETRY_PRESETS = [

{
"AssetClass":"BP_Plane_Wb_C",
"AssetClassPath":"/WorldBuilder/Core/Actors/Placeable/Geometry/BP_Plane_Wb.BP_Plane_Wb_C"
},

{
"AssetClass":"BP_Cone_Wb_C",
"AssetClassPath":"/WorldBuilder/Core/Actors/Placeable/Geometry/BP_Cone_Wb.BP_Cone_Wb_C"
},

{
"AssetClass":"BP_Cube_Wb_C",
"AssetClassPath":"/WorldBuilder/Core/Actors/Placeable/Geometry/BP_Cube_Wb.BP_Cube_Wb_C"
},

{
"AssetClass":"BP_Cylinder_Wb_C",
"AssetClassPath":"/WorldBuilder/Core/Actors/Placeable/Geometry/BP_Cylinder_Wb.BP_Cylinder_Wb_C"
},

{
"AssetClass":"BP_Sphere_Wb_C",
"AssetClassPath":"/WorldBuilder/Core/Actors/Placeable/Geometry/BP_Sphere_Wb.BP_Sphere_Wb_C"
}

]


def random_geometry():
    return random.choice(GEOMETRY_PRESETS)


def generate_geometry(style_rng):

    geometry_assets = []

    base_x = -1500
    base_y = 5000

    spacing = 600

    for i in range(len(GEOMETRY_PRESETS)):

        preset = style_rng.choice(GEOMETRY_PRESETS)

        x = base_x + (i * spacing)
        y = base_y + style_rng.uniform(-200, 200)

        geometry_assets.append({

            "AssetClass": preset["AssetClass"],
            "AssetClassPath": preset["AssetClassPath"],

            "Transform": {

                "Location": {
                    "X": x,
                    "Y": y,
                    "Z": style_rng.uniform(20, 80)
                },

                "Rotation": {
                    "Pitch": 0,
                    "Yaw": style_rng.uniform(-180, 180),
                    "Roll": 0
                },

                "Scale": {
                    "X": style_rng.uniform(0.8, 1.5),
                    "Y": style_rng.uniform(0.8, 1.5),
                    "Z": style_rng.uniform(0.8, 1.5)
                }
            },

            "Material": {
                "RGB": [1,1,1],
                "Metallic": 0,
                "Specular": 0,
                "Roughness": 0,
                "Emissive": 0,
                "WhiteTint": 1
            },

            "OcaData": {
                "CollisionProfile": "BlockAllDynamic",
                "Physics": False,
                "Shadow": True
            }

        })

    return geometry_assets