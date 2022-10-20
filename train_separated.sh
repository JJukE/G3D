OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 PYTHONPATH="/root/graphto3d" PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python \
python ./scripts/train_vaegan.py \
--network_type dis \
--exp ./experiments/saparate_baseline \
--dataset ./GT \
--dataset_3RScan /root/dev/G3D/3RScan \
--path2atlas ./experiments/atlasnet/model_70.pth \
--residual True