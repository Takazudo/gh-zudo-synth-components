#!/usr/bin/env python3
"""Derive browser triangle meshes from retained STEP without modifying originals."""
from pathlib import Path
import hashlib,json
import cadquery as cq
import OCP
ROOT=Path(__file__).resolve().parents[1]
ENTRIES=[
("rk09l1140","sources/history-r06/alps-rk09l1140a5l/RK09L1140-F15.STEP","manufacturer-supplied family geometry"),
("rs20h111c009","sources/history-r06/alps-rs20h111c009/RS20H111C009.STEP","manufacturer-supplied exact-product download"),
("pj398sm","sources/history-r06/qingpu-wqp518ma/PJ398SM-family.step","community family geometry; untested in origin metadata"),
]
def digest(b): return hashlib.sha256(b).hexdigest()
def main():
    dest=ROOT/"corpus/models";dest.mkdir(parents=True,exist_ok=True)
    receipts=[]
    for id,path,scope in ENTRIES:
        source=ROOT/path
        obj=cq.importers.importStep(str(source))
        shapes=obj.vals()
        shape=cq.Compound.makeCompound(shapes)
        bounds=shape.BoundingBox()
        verts,faces=shape.tessellate(0.1,0.3)
        xyz=[[round(v.x,6),round(v.y,6),round(v.z,6)] for v in verts]
        data={"id":id,"positions":xyz,"triangles":faces,
              "bounds_mm":[bounds.xmin,bounds.ymin,bounds.zmin,bounds.xmax,bounds.ymax,bounds.zmax],
              "fidelity":"derived triangulation","source_fidelity":scope,
              "units":"millimetres as imported; no physical fit qualification"}
        output=(json.dumps(data,separators=(",",":"))+"\n").encode()
        out=dest/(id+".json");out.write_bytes(output)
        receipts.append({"id":id,"input":path,"input_sha256":digest(source.read_bytes()),
                         "output":str(out.relative_to(ROOT)),"output_sha256":digest(output),
                         "cadquery":cq.__version__,"ocp":OCP.__version__,
                         "linear_tolerance":0.1,"angular_tolerance":0.3,
                         "imported_top_level_shapes":len(shapes),
                         "solid_count":len(shape.Solids()),
                         "vertex_count":len(verts),"triangle_count":len(faces),
                         "bounds_mm":data["bounds_mm"],"source_scope":scope,
                         "fidelity":"derived","physical_fit":"NOT TESTED"})
        print(id,len(verts),len(faces),flush=True)
    (ROOT/"provenance/step-derivation.json").write_text(json.dumps(receipts,indent=2)+"\n")
if __name__=="__main__": main()
