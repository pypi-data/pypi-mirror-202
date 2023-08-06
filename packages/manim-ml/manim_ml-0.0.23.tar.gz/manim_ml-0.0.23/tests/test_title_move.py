from manim import *
from PIL import Image
from manim_ml.neural_network.layers.feed_forward import FeedForwardLayer
from manim_ml.neural_network.neural_network import NeuralNetwork
import numpy as np

config.pixel_height = 720
config.pixel_width = 1280
config.frame_height = 6.0
config.frame_width = 6.0

class NeuralNetworkScene(Scene):
    """Test Scene for the Neural Network"""

    def construct(self):
        # Make the Layer object
        nn = NeuralNetwork([
            FeedForwardLayer(3),
            FeedForwardLayer(5),
            FeedForwardLayer(3),
        ] , title="Test Title")
        nn.move_to(ORIGIN)
        # Make Animation
        self.add(nn)
        nn.shift(RIGHT)
        nn.move_to(ORIGIN)
        self.wait(2)
        nn.scale(0.5)
        # self.play(Create(nn))
        forward_propagation_animation = nn.make_forward_pass_animation(
            run_time=5, passing_flash=True
        )

        self.play(forward_propagation_animation)
