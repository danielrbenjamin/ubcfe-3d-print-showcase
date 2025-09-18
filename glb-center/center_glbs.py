import trimesh
import os

# Define input/output folders
RAW_DIR = os.path.join("data", "raw_glbs")
OUT_DIR = os.path.join("data", "processed_glbs")

# Make sure output folder exists
os.makedirs(OUT_DIR, exist_ok=True)

def center_glb(file_path, output_path):
    """
    Load a GLB file, move its centroid to origin, and save new file.
    """
    try:
        mesh = trimesh.load(file_path)
        if not isinstance(mesh, trimesh.Trimesh) and hasattr(mesh, "geometry"):
            # Some GLBs are "scenes" with multiple meshes
            combined = trimesh.util.concatenate(tuple(mesh.geometry.values()))
            mesh = combined

        # Move centroid to origin
        mesh.apply_translation(-mesh.centroid)

        # Export to GLB
        mesh.export(output_path)
        print(f"✅ Centered: {os.path.basename(file_path)} → {output_path}")
    except Exception as e:
        print(f"❌ Failed to process {file_path}: {e}")

def main():
    # Process all .glb files in raw_glbs
    for filename in os.listdir(RAW_DIR):
        if filename.lower().endswith(".glb"):
            input_path = os.path.join(RAW_DIR, filename)
            output_path = os.path.join(OUT_DIR, filename)
            center_glb(input_path, output_path)

if __name__ == "__main__":
    main()
