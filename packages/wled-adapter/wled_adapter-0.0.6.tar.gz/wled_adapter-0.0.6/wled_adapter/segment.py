from typing import Union

from colour import Color


class Segment:
    def __init__(self, len: int) -> None:
        """
        Initializes a Segment object with a given length.

        Args:
            len (int): The length of the segment.

        Returns:
            None
        """
        self._colors = [Color("black") for _ in range(len)]
        self._prev_colors = [None for _ in range(len)]
        pass

    def _set_pixel(self, pixel: int, color: Color) -> None:
        """
        Sets the color of a pixel at a given index.

        Args:
            pixel (int): The index of the pixel.
            color (Color): The color to set.

        Returns:
            None

        Raises:
            IndexError: If the pixel index is out of range.
        """
        if pixel < 0 or pixel >= len(self):
            raise IndexError(f"Pixel index {pixel} out of range")
        self._colors[pixel] = color

    def __setitem__(self, key: int, value: Color) -> None:
        """
        Sets the color of a pixel using the [] operator.

        Args:
            key (int): The index of the pixel.
            value (Color): The color to set.

        Returns:
            None
        """
        self._set_pixel(key, value)

    def __getitem__(self, key: int) -> Color:
        """
        Gets the color of a pixel using the [] operator.

        Args:
            key (int): The index of the pixel.

        Returns:
            Color: The color of the pixel.
        """
        return self._colors[key]

    def __delitem__(self, key: int) -> None:
        """
        Raises an error when trying to delete a pixel from the segment.

        Args:
            key (int): The index of the pixel.

        Returns:
            None

        Raises:
            NotImplementedError: Deleting pixels from a segment is not supported.
        """
        raise NotImplementedError("Cannot delete pixels from a segment")

    def __len__(self) -> int:
        """
        Returns the length of the segment.

        Returns:
            int: The length of the segment.
        """
        return self._colors.__len__()

    def set_all(self, color: Color) -> None:
        """
        Sets all pixels in the segment to a given color.

        Args:
            color (Color): The color to set.

        Returns:
            None
        """
        for i in range(len(self)):
            self._set_pixel(i, color)

    def set_range(self, start: int, stop: int, color: Color) -> None:
        """
        Sets a range of pixels in the segment to a given color.

        Args:
            start (int): The starting index of the range.
            stop (int): The ending index of the range.
            color (Color): The color to set.

        Returns:
            None

        Raises:
            IndexError: If the start or stop index is out of range.
        """
        if start < 0 or start >= len(self) or stop < 0 or stop >= len(self):
            raise IndexError(f"Pixel index {start} or {stop} out of range")
        for i in range(start, stop + 1):
            self._set_pixel(i, color)

    def set_off(self) -> None:
        """
        Sets all pixels in the segment to black (off).

        Returns:
            None
        """
        self.set_all(Color("black"))

    def _get_changes(self) -> list[Color]:
        """
        Gets the changes in colors between the current state and the previous state.

        Returns:
            list[Color]: A list of color changes.
        """
        changes = [None] * len(self)
        for i in range(len(self)):
            changes[i] = (
                self._colors[i] if self._colors[i] != self._prev_colors[i] else None
            )

        return changes

    def reset_changes(self) -> None:
        """
        Resets the changes in colors.

        Returns:
            None
        """
        self._prev_colors = self._colors.copy()

    def get_optimised_colour_changes(self) -> Union[int, Color]:
        """
        Returns a list with the optimised colour changes according to
        https://kno.wled.ge/interfaces/json-api/#per-segment-individual-led-control.

        Returns:
            Union[int, Color]: A list with the optimised colour changes.
        """
        changes = [(c, 1) for c in self._get_changes()]
        complete_sequence: Union[int, Color] = []

        last_unique_element = 0
        # group identical colours
        for i in range(1, len(changes)):
            if changes[i][0] and changes[i][0] == changes[last_unique_element][0]:
                changes[last_unique_element] = (
                    changes[i][0],
                    changes[last_unique_element][1] + 1,
                )
                changes[i] = (None, 0)
            else:
                last_unique_element = i

        sequence_started = False
        for i in range(len(changes)):
            if changes[i][1] == 0:
                continue

            # empty spaces, break the sequence
            if not changes[i][0]:
                sequence_started = False
                continue

            # a valid colour, check repetitions
            stop_index = i + changes[i][1] - 1
            colour = changes[i][0]
            # if single element, check if start index was already added
            if stop_index == i:
                if not sequence_started:
                    sequence_started = True
                    complete_sequence.append(i)
            else:
                # range: add start and stop index
                complete_sequence.extend([i, stop_index])
                sequence_started = False
            complete_sequence.append(colour)

        return complete_sequence
