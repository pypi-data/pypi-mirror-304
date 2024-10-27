# 2D Whole-Body Keypoint Models


## BlazePose

### Performance Metrics

| Model   |    AP |   AP<sup>50</sup> |   AP<sup>75</sup> |   AP<sup>L</sup> |    AR |   AR<sup>50</sup> |   AR<sup>75</sup> |   AR<sup>L</sup> |
|---------|-------|-----------|-----------|----------|-------|-----------|-----------|----------|
| Lite    |  0.39 |      1.94 |      0.03 |     0.53 |  2.87 |      9.73 |      1.22 |     2.87 |
| Heavy   |  3.86 |     12.54 |      1.79 |     4.17 |  8.69 |     23.1  |      5.57 |     8.69 |

### Runtime Metrics

| Model   |   Load (ms) |   Inference (ms) |   Postprocess (ms) |   I/O (ms) |
|---------|-------------|------------------|--------------------|------------|
| Lite    |       32.17 |             0    |               0.08 |      48.59 |
| Heavy   |      362.62 |           165.42 |               0.19 |      54.54 |