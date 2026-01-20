import json
from pathlib import Path
import argparse

import os
from PIL import Image


parser = argparse.ArgumentParser(description="eating animation util")
parser.add_argument("-i","--id", type=str,help="item id")
parser.add_argument("-n","--namespace", type=str,help="Namespace")
parser.add_argument("-f","--frames", type=int,help="Frame amount",default=4)

args = parser.parse_args()
item_id = args.id
frames = args.frames
namespace = args.namespace

if not namespace:
    namespace = input("Namespace : ")
if not frames:
    frames = int(input("Frames : "))
if not item_id:
    item_id = input("Item Id : ")

def make_dir(path:Path):
    os.makedirs(path,exist_ok=True)

make_dir(f"assets/eatinganimation/models/item/food/{namespace}/{item_id}")
make_dir(f"assets/eatinganimation/textures/item/food/{namespace}/{item_id}")
make_dir(f"assets/{namespace}/items")
template_path = "template.json"
model_definition_path = f"assets/{namespace}/items/{item_id}.json"

with open(template_path,"r") as template_file:
    template = json.load(template_file)
    with open(model_definition_path,"w") as model_definition_file:
        data = template
        data["model"]["on_false"]["model"] = f"{namespace}:item/{item_id}"
        data["model"]["on_true"]["fallback"]["model"] = f"{namespace}:item/{item_id}"
        threshold = 0.0
        per_frame_threshold = 1.0 / frames
        for i in range(frames):
            threshold += per_frame_threshold
            data["model"]["on_true"]["entries"].append(                {
                        "model": {
                            "type": "minecraft:model",
                            "model": f"eatinganimation:item/food/{namespace}/{item_id}/{item_id}{i}"
                        },
                        "threshold": threshold
                    }
                )
            dst = f"assets/eatinganimation/textures/item/food/{namespace}/{item_id}/{item_id}{i}.png"
            if not Path(dst).exists():
                picture = Image.new('RGBA', (16, 16))
                picture.save(dst)

            with open(f"assets/eatinganimation/models/item/food/{namespace}/{item_id}/{item_id}{i}.json","w") as f:
                json.dump(
                {
                        "parent": "minecraft:item/generated",
                        "textures": {
                        "layer0": f"eatinganimation:item/food/{namespace}/{item_id}/{item_id}{i}"
                        }
                },f,
                indent=2
            )
        json.dump(data,model_definition_file)




