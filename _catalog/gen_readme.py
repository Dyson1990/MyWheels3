# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:00:37 2023

@author: Weave
"""

from pathlib import Path
my_wheels_dir = Path(__file__).parent.parent
content_p = my_wheels_dir/"_catalog"/"content.json"
md_p = my_wheels_dir/"README.md"

import json
import datetime

from pprint import pprint
from loguru import logger

def update_json():
    global my_wheels_dir, content_p
    
    content = json.loads(content_p.read_bytes())
    record_set = set(content["catalog"].keys())
    file_set = set([])
    for p0 in my_wheels_dir.rglob("*.py"):
        fp_parts = list(p0.parts)[len(my_wheels_dir.parts):]
        k0 = Path("/".join(fp_parts))
        file_set.add(k0.as_posix())
        
    removed_files = record_set - file_set
    for k0 in removed_files:
        t0 = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        s0 = f"【remove】 {k0}:{content['catalog'][k0]}"
        content["changing-logs"].append(t0+s0)
        content['catalog'].pop(k0)
        logger.info(s0)
    
    for k0 in file_set:
        if k0 not in content['catalog']:
            t0 = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
            content['catalog'][k0] = ""
            s0 = f"【create】 {k0}"
            content["changing-logs"].append(t0+s0)
            logger.info(s0)
            
    content['catalog'] = {k0: content['catalog'][k0] 
                          for k0 in sorted(content['catalog'])}
        # if len(fp_parts) == 1:
        #     fp_parts.insert(0, "root")
        # elif len(fp_parts) >= 3:
        #     fp_parts = fp_parts[:2] + ["/".join(fp_parts[2:])]
            
        # if len(fp_parts) == 2:
        #     fp_parts.insert(1, "")

    # print(content)
    content_p.write_text(json.dumps(content, indent=2, ensure_ascii=False)
                          , encoding="utf-8")
    
def gen_md():
    global content_p, my_wheels_dir, md_p
    content = json.loads(content_p.read_bytes())
    lines = []
    
    lines.extend(["# MyWheels3", "我的一些代码中需要用到的类"])
    for l0 in content["journal"]:
        lines.append(f"- **{l0[0]}**: {l0[1]}")
    
    lines.extend(["# CATALOG"])
    catalog_dict = {}
    for k0, v0 in content["catalog"].items():
        p0 = my_wheels_dir/k0
        
        if not p0.exists():
            logger.error(f"{p0}不存在！！")
            continue
        
        fp_parts = list(p0.parts)[len(my_wheels_dir.parts):]
        
        if len(fp_parts) == 1:
            fp_parts.insert(0, "root")
        elif len(fp_parts) >= 3:
            # print(fp_parts)
            fp_parts = fp_parts[:2] + ["/".join(fp_parts[2:])]
            
        if len(fp_parts) == 2:
            fp_parts.insert(1, "")
            
        catalog_dict[fp_parts[0]] = catalog_dict.get(fp_parts[0], {})
        d1 = catalog_dict[fp_parts[0]] 
        d1[fp_parts[1]] = d1.get(fp_parts[1], {})
        d2 = d1[fp_parts[1]]
        d2[fp_parts[2]] = d2.get(fp_parts[2], v0)
    
    for k1, d1 in catalog_dict.items():
        lines.append("## "+k1)
            
        for k2, d2 in d1.items():
            if k2:
                # print("k2:", k2)
                lines.append("#### "+k2)
            
            for k3, v3 in d2.items():
                lines.append(f"- **{k3}**: {v3}")
        # break
        
        
        # lines.extend(["## "+fp_parts[0]
        #               , "### "+fp_parts[1] if fp_parts[1] else ""
        #               , "#### "+fp_parts[2]
        #               , v0
        #               ])
    # pprint(catalog_dict)
    md_p.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    update_json()
    gen_md()
    