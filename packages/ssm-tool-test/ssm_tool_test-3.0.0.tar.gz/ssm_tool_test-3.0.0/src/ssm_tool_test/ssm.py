# Definitions of methods to get parameter store from aws
# Note: using aws credentials
from botocore.exceptions import ClientError
from contextlib import AsyncExitStack
from aiobotocore.session import AioSession
import logging


class ManagerParameters():
    def __init__(self):
        self._exit_stack = AsyncExitStack()
    
    @staticmethod
    async def create_ssm_client(session: AioSession, exit_stack: AsyncExitStack):
        # Create client and add cleanup
        client = await exit_stack.enter_async_context(session.create_client('ssm'))
        return client

    async def get_parameters_by_path(self, path):
        session = AioSession()
        async with AsyncExitStack() as exit_stack:
            ssm_client = await self.create_ssm_client(session, exit_stack)
            try:
                params = []
                kwargs = {'Path': path, 'Recursive': True, 'WithDecryption': True}
                paginator = ssm_client.get_paginator('get_parameters_by_path')
                async for page in paginator.paginate(**kwargs):
                    for param in page['Parameters']:
                        params.append(param)
                return params
            except ClientError as e:
                logging.error(f"Error: {e}")
