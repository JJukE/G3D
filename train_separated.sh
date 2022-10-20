OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 PYTHONPATH="/root/graphto3d" PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
python /root/graphto3d/scripts/train_vaegan.py \
--network_type dis \
--exp /root/graphto3d/experiments/saparate_baseline \
--dataset /root/dev/G3D/GT \
--dataset_3RScan /root/dev/G3D/3RScan \
--path2atlas /root/graphto3d/experiments/atlasnet/model_70.pth \
--residual True