from typing import Literal
import customtkinter as ctk

from .gradient import Gradient, LEFT_TO_RIGHT, TOP_TO_BOTTOM, RADIAL

class GradientFrame(ctk.CTkFrame):
    """
    A custom frame with a gradient background.

    Inherits from CTkFrame and provides a gradient background
    defined by the specified colors and direction.

    Parameters:
        master (ctk.Widget): The parent widget of the frame.
        width (int): The width of the frame.
        height (int): The height of the frame.
        direction (str): The direction of the gradient (e.g., 'horizontal', 'vertical').
        colors (list): A list of colors to be used in the gradient.
        corner_radius (int, optional): The radius of the corners of the frame. Defaults to 0.

    Example:
        ```python
        gradient_frame = GradientFrame(
            master = root,
            width = 300,
            height = 200,
            direction = 'horizontal',
            colors = ('#FF0000', '#0000FF')
        )
        ```
    """

    def __init__(
            self,
            master,
            width: int,
            height: int,
            direction: Literal[
                "horizontal",
                "vertical",
                "radial"
            ],
            colors: tuple,
            corner_radius = 0
        ):

        if corner_radius > 10:
            corner_radius = 10

        super().__init__(
            master,
            corner_radius = corner_radius,
            height = height,
            width = width
        )

        first_color_frame = ctk.CTkFrame(
            master = self,
            corner_radius = corner_radius,
            fg_color = colors[0]
        )

        second_color_frame = ctk.CTkFrame(
            master = self,
            corner_radius = corner_radius,
            fg_color = colors[1]
        )

        if direction == "vertical":
            direction = 1

        if direction == "horizontal":
            direction = 2

        if direction == "radial":
            direction = 3

        self.gradient = Gradient(
            master = self,
            direction = direction,
            height = height,
            colors = colors,
            width = width
        )

        # TODO: Make some calculations regarding the border radius so that it extends
        # the gradient frame and do not have the visual error appropriately.

        if direction == LEFT_TO_RIGHT:
            first_color_frame.pack(fill = "y", side = "left")
            second_color_frame.pack(fill = "y", side = "right")
            self.gradient.place(relx = 0.02, rely = 0, relwidth = 0.96, relheight = 1)

        if direction == TOP_TO_BOTTOM:
            first_color_frame.pack(fill = "x", side = "top")
            second_color_frame.pack(fill = "x", side = "bottom")
            self.gradient.place(relx = 0, rely = 0.02, relwidth = 1, relheight = 0.96)

        if direction == RADIAL:
            second_color_frame.pack(fill = "both", side = "top", expand = True)
            self.gradient.place(relx = 0.02, rely = 0, relwidth = 0.96, relheight = 1)
