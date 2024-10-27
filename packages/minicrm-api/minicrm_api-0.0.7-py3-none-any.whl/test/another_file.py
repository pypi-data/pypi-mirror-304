from ..minicrm_api import MiniCrmClient

client = MiniCrmClient(76354, "fGD6Tj5aEwFc0WzdJ3QCerPSBxpuOHXo")

adatlap = client.get_adatlap_details(168)
print(adatlap)
