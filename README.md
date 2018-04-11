# xmlmeta
Metaclass based entities generator. Based on Elementtree.

Example:

```python
import xml.etree.ElementTree as ET

from metaentity import *

tree = ET.parse(file)

root = tree.getroot()

root_entity = build_entity(root)
```
