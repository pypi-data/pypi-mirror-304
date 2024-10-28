# auto-generated file
import asyncio
import json
from cardinal_sdk.model import Permission
from cardinal_sdk.kotlin_types import DATA_RESULT_CALLBACK_FUNC, symbols
from typing import List
from cardinal_sdk.model.CallResult import create_result_from_json, interpret_kt_error
from ctypes import cast, c_char_p

class PermissionApi:

	def __init__(self, cardinal_sdk):
		self.cardinal_sdk = cardinal_sdk

	async def modify_user_permissions_async(self, user_id: str, permissions: Permission) -> List[Permission]:
		loop = asyncio.get_running_loop()
		future = loop.create_future()
		def make_result_and_complete(success, failure):
			if failure is not None:
				result = Exception(failure.decode('utf-8'))
				loop.call_soon_threadsafe(lambda: future.set_exception(result))
			else:
				result = [Permission._deserialize(x1) for x1 in json.loads(success.decode('utf-8'))]
				loop.call_soon_threadsafe(lambda: future.set_result(result))
		payload = {
			"userId": user_id,
			"permissions": permissions.__serialize__(),
		}
		callback = DATA_RESULT_CALLBACK_FUNC(make_result_and_complete)
		loop.run_in_executor(
			self.cardinal_sdk._executor,
			symbols.kotlin.root.com.icure.cardinal.sdk.py.api.PermissionApi.modifyUserPermissionsAsync,
			self.cardinal_sdk._native,
			json.dumps(payload).encode('utf-8'),
			callback
		)
		return await future

	def modify_user_permissions_blocking(self, user_id: str, permissions: Permission) -> List[Permission]:
		payload = {
			"userId": user_id,
			"permissions": permissions.__serialize__(),
		}
		call_result = symbols.kotlin.root.com.icure.cardinal.sdk.py.api.PermissionApi.modifyUserPermissionsBlocking(
			self.cardinal_sdk._native,
			json.dumps(payload).encode('utf-8'),
		)
		result_info = create_result_from_json(cast(call_result, c_char_p).value.decode('utf-8'))
		symbols.DisposeString(call_result)
		if result_info.failure is not None:
			raise interpret_kt_error(result_info.failure)
		else:
			return_value = [Permission._deserialize(x1) for x1 in result_info.success]
			return return_value
