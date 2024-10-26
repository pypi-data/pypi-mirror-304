# accelapy
An Accela specific API for https://developer.accela.com/docs/api_reference/api-index.html

## How to use:

You may need to get your payload from Accela for your environment.

```python
from accelapy.accelapy.client import AccelaClient
from accelapy.accelapy.records_client.types import Response
from accelapy.accelapy.records_client.models import RecordModel
import json
from typing import List
from accelapy.accelapy.payload import Payload

payload = Payload(payload_str='totally-real-payload')
api_client = AccelaClient(payload=payload)
response: Response = api_client.v4_get_records.sync_detailed(client=api_client.authentication_client, custom_id='E24-00103')
json_load = json.loads(response.content)
record_models : List[RecordModel] = [RecordModel.from_dict(x) for x in json_load['result']]
print(record_models)
```
