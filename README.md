# cvat_on_lima_vm

Build a VM with lima and run CVAT and Automatic Annotation.

## Initial Setup

1. fix `metadata.annotations.spec` [yolox/function.yaml](yolox/function.yaml)
1. Put the model in `yolox/best_ckpt.pth`.
1. `limactl start --name=cvat lima.yaml`
1. Wait for lima VM to start.
1. `limactl shell cvat`
1. `sudo ./docker_run.sh` You must enter the cvat admin password at the end of the run.

## Reference

- [lima/default\.yaml at master · lima\-vm/lima](https://github.com/lima-vm/lima/blob/master/examples/default.yaml)
- [lima/docker\.yaml at master · lima\-vm/lima](https://github.com/lima-vm/lima/blob/master/examples/docker.yaml)
- [Semi\-automatic and Automatic Annotation \| CVAT](https://openvinotoolkit.github.io/cvat/docs/administration/advanced/installation_automatic_annotation/)
