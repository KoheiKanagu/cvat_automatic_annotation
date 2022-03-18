# cvat_automatic_annotation

Nuclio script to execute YOLOX on CVAT Automatic Annotation.

## deploy

1. fix `metadata.annotations.spec` [yolox/function.yaml](yolox/function.yaml)
1. Put the model in `yolox/best_ckpt.pth`.
1. `./cvat/serverless/deploy_cpu.sh /YOU/PATH/cvat_automatic_annotation/yolox`

## Reference

[Semi\-automatic and Automatic Annotation \| CVAT](https://openvinotoolkit.github.io/cvat/docs/administration/advanced/installation_automatic_annotation/)
