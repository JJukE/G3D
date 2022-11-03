from __future__ import print_function
import open3d as o3d # open3d needs to be imported before other packages!
import argparse
import os
import random
import numpy as np

from helpers.util import bool_flag, batch_torch_denormalize_box_params
from helpers.metrics import validate_constrains, validate_constrains_changes, estimate_angular_std
from helpers.visualize_graph import run as vis_graph
from helpers.visualize_scene import render
import helpers.retrieval as retrieval

import json

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', required=False, type=str, default="./GT", help="dataset path")
parser.add_argument('--exp', default='./experiments/layout_test', help='experiment name')
args = parser.parse_args()

def visualize_graph_practice():
    # scene graph visualization. saves a picture of each graph to the outfolder
    scan = "f62fd5fd-9a3f-2f44-883a-1e5cf819608e"
    colormap = vis_graph(use_sampled_graphs=False, scan_id=scan, split=None, data_path=args.dataset,
                            outfolder=args.exp + "/vis_graphs/")
    colors = []
    # convert colors to expected format
    def hex_to_rgb(hex):
        hex = hex.lstrip('#')
        hlen = len(hex)
        return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))
    for i in instances:
        h = colormap[str(i)]
        rgb = hex_to_rgb(h)
        colors.append(rgb)
    colors = np.asarray(colors) / 255.

    # layout and shape visualization through open3d
    render(boxes_pred_den, angles_pred, classes=vocab['object_idx_to_name'], render_type='points', classed_idx=dec_objs,
            shapes_pred=shapes_pred.cpu().detach(), colors=colors, render_boxes=True)

if __name__=="__main__": visualize_graph_practice()