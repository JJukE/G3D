import os
import open3d as o3d
import numpy as np
from helpers.util import fit_shapes_to_box, params_to_8points, params_to_8points_no_rot
import json
import torch
from render.lineMesh import LineMesh


def render(predBoxes, predAngles=None, classes=None, classed_idx=None, shapes_pred=None, render_type='points',
           render_shapes=True, render_boxes=False, colors=None, scene_index=0, scan_id=None):

    if render_type not in ['meshes', 'points']:
        raise ValueError('Render type needs to be either set to meshes or points.')

    if colors is None:
        colors = np.asarray(json.load(open('graphs/color_palette.json', 'r'))['rgb']) / 255.

    vis = o3d.visualization.Visualizer()
    # vis.create_window(visible=False)

    # ren_opt = vis.get_render_option()
    # ren_opt.mesh_show_back_face = True
    # ren_opt.line_width = 50.

    edges = [0, 1], [0, 2], [0, 4], [1, 3], [1, 5], [2, 3], [2, 6], [3, 7], [4, 5], [4, 6], [5, 7], [6, 7]

    valid_idx = []
    all_pcl = []
    
    # print('shape of predBoxes: ', predBoxes.shape)
    # print('shape of shapes_pred: ', shapes_pred.shape)
    faces = None
    did_fit = None
    points = o3d.geometry.PointCloud()
    shapes = o3d.geometry.TriangleMesh()
    shapes_with_box = o3d.geometry.TriangleMesh()
    for i in range(len(predBoxes)-1):
        shape = shapes_pred[i]
        # print('shape of shape: ', shape.shape)
        do_render_shape = True
        if render_type == 'points':
            vertices = shape
        else:
            do_render_shape = False
            if shape is not None:
                if len(shape) == 2:
                    vertices, faces = shape
                    did_fit = True
                    do_render_shape = True
                elif len(shape) == 3:
                    vertices, faces, did_fit = shape
                    do_render_shape = True
                else:
                    do_render_shape = False

        if classes[classed_idx[i]].split('\n')[0] in ["ceiling", "door", "doorframe"]:
            continue

        if predAngles is None:
            box_points = params_to_8points_no_rot(predBoxes[i])
        else:
            box_and_angle = torch.cat([predBoxes[i].float(), predAngles[i].float()])
            box_points = params_to_8points(box_and_angle, degrees=True)

        if do_render_shape:
            if predAngles is None:
                denorm_shape = fit_shapes_to_box(predBoxes[i], vertices, withangle=False)
            else:
                box_and_angle = torch.cat([predBoxes[i].float(), predAngles[i].float()])
                denorm_shape = fit_shapes_to_box(box_and_angle, vertices)

        valid_idx.append(i)
        if render_type == 'points':
            pcd_shape = o3d.geometry.PointCloud()
            pcd_shape.points = o3d.utility.Vector3dVector(denorm_shape)
            all_pcl += denorm_shape.tolist()
            pcd_shape_colors = [colors[i % len(colors)] for _ in range(len(denorm_shape))]
            pcd_shape.colors = o3d.utility.Vector3dVector(pcd_shape_colors)
            
            points += pcd_shape
            
            if render_shapes:
                vis.add_geometry(pcd_shape)
        else:
            if faces is not None:
                mesh = o3d.geometry.TriangleMesh()
                mesh.triangles = o3d.utility.Vector3iVector(faces)
                mesh.vertices = o3d.utility.Vector3dVector(denorm_shape)
                pcd_shape_colors = [colors[i % len(colors)] for _ in range(len(denorm_shape))]
                mesh.vertex_colors = o3d.utility.Vector3dVector(pcd_shape_colors)

                if did_fit:
                    mesh = mesh.subdivide_loop(number_of_iterations=1)
                    mesh = mesh.filter_smooth_taubin(number_of_iterations=10)
                mesh.compute_vertex_normals()
                
                shapes += mesh
                shapes_with_box += mesh
                
                if render_shapes:
                    vis.add_geometry(mesh)

        if (len(shape)==2 or len(shape)==3) and render_boxes:
            line_colors = [colors[i % len(colors)] for _ in range(len(edges))]
            line_mesh = LineMesh(box_points, edges, line_colors, radius=0.02)
            line_mesh_geoms = line_mesh.cylinder_segments

            for g in line_mesh_geoms:
                shapes_with_box += g
                vis.add_geometry(g)
        
        # save as file
        o3d.io.write_point_cloud(os.path.join("/root/graphto3d/viz/", str(scene_index) + "_" + str(scan_id) + "_pc.ply"), points)
        if faces is not None:
            o3d.io.write_triangle_mesh(os.path.join("/root/graphto3d/viz/", str(scene_index) + "_" + str(scan_id) + "_mesh.ply"), shapes)
        if faces is not None and (len(shape)==2 or len(shape)==3):
            o3d.io.write_triangle_mesh(os.path.join("/root/graphto3d/viz/", str(scene_index) + "_" + str(scan_id) + "_mesh_with_box.ply"), shapes_with_box)

    # vis.add_geometry(o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.6, origin=[0, 0, 2]))
    # o3d.io.write_point_cloud("/root/graphto3d/viz/pc.pcd", vis)
    # o3d.io.write_triangle_mesh("/root/graphto3d/viz/mesh.ply", vis)
    # o3d.io.write_triangle_mesh("/root/graphto3d/viz/textured_mesh.obj", vis, write_triangle_uvs=True)
    # vis.capture_screen_image("/root/graphto3d/viz/image.jpg", do_render=True)
    # vis.poll_events()
    # vis.run()
    # vis.destroy_window()
