from abc import ABC, abstractmethod


class Decoder(ABC):
    """Base class for all decoders.

    Decoders are used to decode the prediction of pose models into a keypoint list
    in the image coordinate system. The keypoint list is a list of tuples (x, y, score)
    where x and y are the coordinates and score is the prediction confidence.

    All decoders must implement the decode method. Each model has a corresponding decoder,
    and the decode method is automatically called when the model is used for prediction.
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def decode(self, prediction, image_shape):
        pass
