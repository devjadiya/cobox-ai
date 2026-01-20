def validate_scene(scene: dict):
    assert len(scene["Segments"]) > 50, "Scene too short"
