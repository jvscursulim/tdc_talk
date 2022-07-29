

class LightsOut:
    """Lights out class."""
    
    def __init__(self, layout: list) -> None:
        """
        Args:
            layout (list): The initial distribution of
            of the lights in the game.

        Raises:
            TypeError: If layout is not a list.
        """
        if isinstance(layout, list):
            
            self.layout = layout
        else:
            
            raise TypeError("layout is not a list!")
        
        
    def layout_length(self) -> int:
        """Returns the length of the layout.

        Returns:
            int: The layout length.
        """
        
        return len(self.layout)