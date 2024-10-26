from colour import Color

from wled_adapter.connection import Connection
from wled_adapter.segment import Segment
from wled_adapter.state import Seg, State, WledData


class Adapter:
    """
    Represents an adapter for controlling WLED segments using a specified interface.

    Args:
        interface (Connection): The interface used for communication with the WLED
        device.

    Attributes:
        _interface (Connection): The interface used for communication with the WLED
        device.
        _segments (dict[int, Segment]): A dictionary of segments, where the key is the
        segment ID and the value is a Segment object.

    """

    def __init__(self, interface: Connection):
        self._interface = interface
        self._segments: dict[int, Segment] = {}

    def init(self):
        """
        Initializes the adapter by starting the interface.
        """
        self._interface.start()

    def cleanup(self):
        """
        Cleans up the adapter by stopping the interface.
        """
        self._interface.stop()

    @property
    def segments(self):
        """
        Returns the dictionary of segments.
        """
        return self._segments

    def initialise_segments(self):
        """
        Initializes the segments based on the current status received from the WLED
        device.
        """
        state = self.get_state()
        # reset the current segment state
        self._segments = {}

        for segment in state.state.seg:
            segment_len = 0
            if hasattr(segment, "len"):
                segment_len = segment.len
            else:
                segment_len = segment.stop - segment.start
            self._segments[segment.id] = Segment(segment_len)

    def get_state(self) -> WledData:
        """
        Retrieves the state of the WLED device.

        Returns:
            WledData: The state of the WLED device.
        """
        status_json = self._interface.get_wled_status()
        status = WledData.from_json(status_json)
        return status

    def update_segment(self, segment_id: int):
        """
        Updates the specified segment colour state on the WLED device.

        Args:
            segment_id (int): The ID of the segment to update.
        """
        segment = self._segments[segment_id]
        colors = segment.get_optimised_colour_changes()

        colors = [Color(c).hex_l[1:] if isinstance(c, Color) else c for c in colors]
        request = State(seg=[Seg(id=segment_id, i=colors)])
        self.send_state(request)
        segment.reset_changes()

    def send_state(self, state: State):
        """
        Sends the specified state to the WLED device.

        Args:
            state (State): The state to send.
        """
        json = state.to_json(skipkeys=True)
        self._interface.send(json)
