# from iamdata import IAMData
# IAMData().services.get_service_keys()

# IAMData().actions.get_actions_for_service("s3")
# IAMData().actions.action_exists("s3", "GetObject")
# IAMData().actions.get_action_details("s3", "GetObject")

# IAMData().conditions.get_condition_keys_for_service("s3")
# IAMData().conditions.condition_key_exists("s3", "s3:AccessGrantsInstanceArn")
# IAMData().conditions.get_condition_key_details("s3", "s3:AccessGrantsInstanceArn")

# IAMData().resources.get_resource_types_for_service("s3")
# IAMData().resources.resource_type_exists("s3", "Bucket")
# IAMData().resources.get_resource_type_details("s3", "Bucket")

from iamdata import IAMData

iam_data = IAMData()
print(f"Data Version {iam_data.data_version()} updated at {iam_data.data_updated_at()}")
for service_key in iam_data.services.get_service_keys():
    service_name = iam_data.services.get_service_name(service_key)
    print(f"Getting Actions for {service_name}")
    for action in iam_data.actions.get_actions_for_service(service_key):
        action_details = iam_data.actions.get_action_details(service_key, action)
        print(f"{service_key}:{action} => {action_details}")