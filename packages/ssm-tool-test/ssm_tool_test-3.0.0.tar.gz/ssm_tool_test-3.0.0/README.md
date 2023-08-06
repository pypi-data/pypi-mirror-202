# Tool to get SSM parameter store (test)

This is a simple example package to get parameter store from aws account.
Using boto3 and credentials from aws.

### Definitions

- **get_parameters_by_path(attributes)**
    params:
    - attributes: Path of ssm parameters (string)


### USAGE:
```
from ssm_tool_test import ssm
import asyncio

async def main():
    manager = ManagerParameters()
    path = '/path-test/test'
    params = await manager.get_parameters_by_path(path)
    print(params)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

##### by jdroldan@playvox.com