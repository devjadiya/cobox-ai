from app.llm.openai_client import enhance_scene

scene = enhance_scene(scene, intent.get("notes",""))
