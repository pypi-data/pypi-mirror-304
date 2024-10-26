# WLED Adapter Package

## Overview

The `wled_adapter` package is designed to ...

## Installation

To install the `wled_adapter` package, you can use the following command:

```bash
pip install wled_adapter
```

## Usage

Here's a basic example of how to use the `wled_adapter` package:

```python
from wled_adapter import Adapter
adapter.initialise_segments()
adapter = Adapter(SerialConnection(port, 115200))
adapter.segments[0]._set_pixel(0, Color("blue"))
adapter.update_segment(segment)
```
A complete example is available under [examples](examples)
## License

The `wled_adapter` package is licensed under the [MIT License](LICENSE).
