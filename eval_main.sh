OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 PYTHONPATH="/root/graphto3d" PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
python /root/graphto3d/scripts/evaluate_vaegan.py \
--dataset_3RScan /root/dev/G3D/3RScan \
--exp /root/graphto3d/experiments/model_221124 \
--with_points True --with_feats True --epoch 100 \
--path2atlas /root/graphto3d/experiments/atlasnet/model_70.pth \
--evaluate_diversity True --visualize True --export_3d True \
--debug_mode False