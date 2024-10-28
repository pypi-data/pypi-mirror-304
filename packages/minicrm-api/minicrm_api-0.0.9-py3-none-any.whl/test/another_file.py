from ..minicrm_api import MiniCrmClient

client = MiniCrmClient(76354, "fGD6Tj5aEwFc0WzdJ3QCerPSBxpuOHXo")

adatlap = client.get_address(71)
print(adatlap)
