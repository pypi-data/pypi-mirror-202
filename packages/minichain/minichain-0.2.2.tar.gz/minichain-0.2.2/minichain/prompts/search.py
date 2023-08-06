from minichain import Prompt, Output, Input, Request
import numpy as np
class Embedding(Prompt[Input, Output]):
    """
    A prompt that replaces parse with `find` that takes an embedding.
    """

    def parse(self, response: str, inp: Input) -> Output:
        return self.find(response, inp)

    def find(self, response: np.ndarray, inp: Input) -> Output:
        """
        Convert from the embedding response of the function
        to the output type.
        """
        raise NotImplementedError


