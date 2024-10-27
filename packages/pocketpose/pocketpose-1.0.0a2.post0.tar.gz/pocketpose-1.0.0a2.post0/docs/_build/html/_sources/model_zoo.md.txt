# Models

PocketPose provides a collection of pre-trained models for various tasks. You can use them directly for inference in your desktop or mobile applications.

The model zoo is still under construction. More details will be added soon.

| Model                 | Variant    | Inputs    | Outputs                                  |   Precision |   Size (MB) |   FLOPs (M) |   Params (M) |
|-----------------------|------------|-----------|------------------------------------------|-------------|-------------|-------------|--------------|
| baseline-50           | 256x192_17 | 3x192x256 | 17x48x64                                 |           1 |       32.83 |     8041.66 |        23.49 |
| blazepose-full        | 256x256_33 | 256x256x3 | 195, 1, 256x256x1, 64x64x39, 117         |           2 |        6.14 |      774.26 |         3.17 |
| blazepose-heavy       | 256x256_33 | 256x256x3 | 195, 1, 256x256x1, 64x64x39, 117         |           2 |       26.43 |     3858.81 |        13.75 |
| blazepose-lite        | 256x256_33 | 256x256x3 | 195, 1, 256x256x1, 64x64x39, 117         |           2 |        2.69 |      397.56 |         1.36 |
| efficientpose-i       | 256x256_16 | 256x256x3 | 32x32x28, 32x32x16, 32x32x16, 256x256x16 |           2 |        1.43 |     1495.89 |         0.69 |
| efficientpose-i-lite  | 256x256_16 | 256x256x3 | 256x256x16                               |           2 |        1.1  |     1360    |         0.55 |
| efficientpose-ii      | 368x368_16 | 368x368x3 | 46x46x28, 46x46x16, 46x46x16, 368x368x16 |           2 |        3.37 |     7305.14 |         1.67 |
| efficientpose-ii-lite | 368x368_16 | 368x368x3 | 368x368x16                               |           2 |        2.74 |     6883.47 |         1.4  |
| efficientpose-iii     | 480x480_16 | 480x480x3 | 60x60x28, 60x60x16, 60x60x16, 480x480x16 |           2 |        6.24 |    22606.7  |         3.14 |
| efficientpose-iv      | 600x600_16 | 600x600x3 | 75x75x28, 75x75x16, 75x75x16, 600x600x16 |           2 |       12.56 |    71566.1  |         6.41 |
| efficientpose-rt      | 224x224_16 | 224x224x3 | 28x28x28, 28x28x16, 28x28x16, 224x224x16 |           2 |        0.92 |      739.09 |         0.43 |
| efficientpose-rt-lite | 224x224_16 | 224x224x3 | 224x224x16                               |           2 |        0.75 |      721.71 |         0.37 |
| efficientposenas-a    | 256x192_17 | 3x192x256 | 17x48x64                                 |           1 |        1.49 |      726.3  |         1.15 |
| efficientposenas-b    | 256x192_17 | 3x192x256 | 17x48x64                                 |           1 |        3.52 |     1980.43 |         3.03 |
| efficientposenas-b    | 256x256_16 | 3x256x256 | 16x64x64                                 |           1 |        3.52 |     2640.31 |         3.03 |
| efficientposenas-c    | 256x192_17 | 3x192x256 | 17x48x64                                 |           1 |        5.34 |     2681.48 |         4.77 |
| efficientposenas-c    | 256x256_16 | 3x256x256 | 16x64x64                                 |           1 |        5.34 |     3575.04 |         4.77 |
| litehrnet-18          | 256x192_17 | 3x192x256 | 17x48x64                                 |           1 |        1.77 |      406.01 |         1.11 |
| movenet-lightning     | 192x192_17 | 192x192x3 | 1x17x3                                   |           4 |        8.94 |      541.61 |         2.32 |
| movenet-lightning16   | 192x192_17 | 192x192x3 | 1x17x3                                   |           2 |        4.54 |      541.61 |         2.32 |
| movenet-lightning8    | 192x192_17 | 192x192x3 | 1x17x3                                   |           1 |        2.76 |      541.61 |         2.32 |
| movenet-thunder       | 256x256_17 | 256x256x3 | 1x17x3                                   |           4 |       23.87 |     2440.7  |         6.23 |
| movenet-thunder16     | 256x256_17 | 256x256x3 | 1x17x3                                   |           2 |       12    |     2440.7  |         6.23 |
| movenet-thunder8      | 256x256_17 | 256x256x3 | 1x17x3                                   |           1 |        6.8  |     2440.7  |         6.23 |
| posenet-mobilenet100  | 257x257_17 | 257x257x3 | 9x9x17, 9x9x34, 9x9x32, 9x9x32           |           4 |       12.65 |     1674.53 |         3.31 |
| res50                 | 256x192_17 | 3x192x256 | 17x48x64                                 |           1 |       32.83 |     8041.66 |        23.49 |

![Models Timeline](images/model_timeline.png)

| Model         | Variant                   | Inputs    | Outputs                               |   Precision |   Size (MB) |   FLOPs (M) |   Params (M) |
|---------------|---------------------------|-----------|---------------------------------------|-------------|-------------|-------------|--------------|
| BlazePose     | Full                      | 256x256x3 | 195, 1, 256x256x1, 64x64x39, 117      |           2 |        6.14 |      774.26 |         3.17 |
| BlazePose     | Heavy                     | 256x256x3 | 195, 1, 256x256x1, 64x64x39, 117      |           2 |       26.43 |     3858.81 |        13.75 |
| BlazePose     | Lite                      | 256x256x3 | 195, 1, 256x256x1, 64x64x39, 117      |           2 |        2.69 |      397.56 |         1.36 |
| EfficientPose | A_COCO                    | 3x192x256 | 17x48x64                              |           1 |        1.49 |      726.3  |         1.15 |
| EfficientPose | B_COCO                    | 3x192x256 | 17x48x64                              |           1 |        3.52 |     1980.43 |         3.03 |
| EfficientPose | B_MPII                    | 3x256x256 | 16x64x64                              |           1 |        3.52 |     2640.31 |         3.03 |
| EfficientPose | C_COCO                    | 3x192x256 | 17x48x64                              |           1 |        5.34 |     2681.48 |         4.77 |
| EfficientPose | C_MPII                    | 3x256x256 | 16x64x64                              |           1 |        5.34 |     3575.04 |         4.77 |
| MoveNet       | MultiPose-Lightning-FP16  | 1x1x3     | 6x56                                  |           2 |        9.14 |        9.4  |         4.72 |
| MoveNet       | SinglePose-Lightning      | 192x192x3 | 1x17x3                                |           4 |        8.94 |      541.61 |         2.32 |
| MoveNet       | SinglePose-Lightning-FP16 | 192x192x3 | 1x17x3                                |           2 |        4.54 |      541.61 |         2.32 |
| MoveNet       | SinglePose-Lightning-INT8 | 192x192x3 | 1x17x3                                |           1 |        2.76 |      541.61 |         2.32 |
| MoveNet       | SinglePose-Thunder        | 256x256x3 | 1x17x3                                |           4 |       23.87 |     2440.7  |         6.23 |
| MoveNet       | SinglePose-Thunder-FP16   | 256x256x3 | 1x17x3                                |           2 |       12    |     2440.7  |         6.23 |
| MoveNet       | SinglePose-Thunder-INT8   | 256x256x3 | 1x17x3                                |           1 |        6.8  |     2440.7  |         6.23 |
| PoseNet       | MobileNet-075             | 353x257x3 | 23x17x17, 23x17x34, 23x17x64, 23x17x1 |           4 |        4.82 |     1358.86 |         1.26 |
| PoseNet       | MobileNet-100             | 257x257x3 | 9x9x17, 9x9x34, 9x9x32, 9x9x32        |           4 |       12.65 |     1674.53 |         3.31 |
| litehrnet     | 18_coco_256x192           | 3x192x256 | 17x48x64                              |           1 |        1.77 |      406.01 |         1.11 |
| litehrnet     | 18_coco_384x288           | 3x288x384 | 17x72x96                              |           1 |        1.77 |      913.26 |         1.11 |
| litehrnet     | 18_mpii_256x256           | 3x256x256 | 16x64x64                              |           1 |        1.77 |      540.95 |         1.11 |
| litehrnet     | 30_coco_256x192           | 3x192x256 | 17x48x64                              |           1 |        2.83 |      634.08 |         1.74 |
| litehrnet     | 30_coco_384x288           | 3x288x384 | 17x72x96                              |           1 |        2.83 |     1426.24 |         1.74 |
| litehrnet     | 30_mpii_256x256           | 3x256x256 | 16x64x64                              |           1 |        2.83 |      844.99 |         1.74 |

![Performance Comparison](images/performance_comparison.png)
