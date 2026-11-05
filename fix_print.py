from pathlib import Path
content = Path("scratch_inspect_hair.py").read_text(encoding="utf-8")
content = content.replace("print(f\"Material {m_i}: {m_name} ({m_name_en}) - {len(unique_v)} verts:\")", "print(f\"Material {m_i}: {m_name_en} - {len(unique_v)} verts:\")")
Path("scratch_inspect_hair.py").write_text(content, encoding="utf-8")
