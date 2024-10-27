# Understanding the Dataflow

This document describes the dataflow of the project. It is intended to help contributors understand the project structure and how to contribute to the project.

The Python package of PocketPose is intended for model preparation and performance evaluation. Complementing this, the `pocketpose-android` package, which is under active development, will enable seamless integration of these optimized models into Android applications.

```{mermaid}
graph LR
    A[pocketpose-android] -- Uses --> B[Converted Models]
    C[pocketpose] -- Converts & Optimizes --> B
    C -- Benchmarks & Evaluates --> D[Datasets]
    E[Model Factory] -- Creates --> F[Model Instances]
    G[Converters] -- Converts --> F
    H[Inferencer] -- Infers Poses --> I[Images/Videos]
    F -- Used by --> H

    style C fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#bbf,stroke:#333,stroke-width:2px
    style H fill:#bbf,stroke:#333,stroke-width:2px
```

```{mermaid}
graph TD
    A[Model Sources e.g., PyTorch Models] -- Conversion --> B[Converters]
    B -- Produces --> C[Mobile-Optimized Models e.g., TFLite]
    C -- Integrated into --> D[Model Registry]
    E[Model Factory] -- Instantiates --> C
    F[Benchmark Scripts] -- Evaluate --> C
    G[Datasets e.g., COCO] -- Used in --> F
    C -- Deployed to --> H[pocketpose-android]

    style B fill:#f96,stroke:#333,stroke-width:2px
    style D fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#bbf,stroke:#333,stroke-width:2px
    style F fill:#f96,stroke:#333,stroke-width:2px
```