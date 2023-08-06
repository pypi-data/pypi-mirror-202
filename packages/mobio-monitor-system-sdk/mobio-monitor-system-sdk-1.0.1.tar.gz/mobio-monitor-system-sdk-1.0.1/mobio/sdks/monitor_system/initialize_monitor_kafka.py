import json
import os

APPLICATION_DATA_DIR = os.environ.get("APPLICATION_DATA_DIR")
FOLDER_INFORMATION_CONSUMER_DATA_SHARE = 'MonitorSystem/'
FOLDER_INFORMATION_CONSUMER = 'info-consumer/'
FOLDER_INFORMATION_CONSUMER_NOT_MONITOR = 'info-consumer-not-monitor/'

STORE_DATA_INFO_CONSUMER = '/info_consumer.json'
STORE_DATA_INFO_CONSUMER_NOT_MONITOR = '/info_consumer_not_monitor.json'

WORKING_DIR = str(os.environ.get("MOBIO_TEMPLATE_HOME"))

# Thông tin của tất cả consumer
"""
    - module_name các từ phải ngăn cách nhau bởi GẠCH CHÂN (_) hoặc GẠCH NGANG (-)
    {
        'module_name': tên module,
        'infor_consumer': danh sách thông tin consumer
    }
    
    Example:
    {
        'module_name': 'journey_builder',
        'info_consumer': [
            {'group': 'jb-operation-cmd-group', 'topic': 'jb-start-cmd'},
            {'group': 'jb-operation-cmd-group', 'topic': 'jb-validate-cmd'}
        ]
    }
"""

# Thông tin của consumer không muốn  gửi thông báo về
"""
    - module_name các từ phải ngăn cách nhau bởi GẠCH CHÂN (_) hoặc GẠCH NGANG (-)
    - module_name sẽ được sử dụng làm tên channel slack dưới dạng LOWER CASE
    {
        'module_name': tên module,
        'infor_consumer': danh sách các consumer không muốn monitor
    }
        
    Example:
    {
        'module_name': 'journey_builder',
        'info_consumer': [
            {'group': 'jb-operation-cmd-group', 'topic': 'jb-start-cmd'},
            {'group': 'jb-operation-cmd-group', 'topic': 'jb-validate-cmd'}
        ]
    }
"""


class InitializeMonitorKafka:

    def __init__(self, name_space_working):
        self.working_dir = str(os.environ.get(name_space_working))

    @staticmethod
    def read_json_file(path_file):
        f = open(path_file)
        data = json.load(f)
        return data if data else {}

    def read_data_info_consumer(self):
        vm_type = os.environ.get("VM_TYPE")
        path_file = self.working_dir + '/monitor_kafka' + '/' + vm_type.upper() + STORE_DATA_INFO_CONSUMER
        data = InitializeMonitorKafka.read_json_file(path_file)
        return data

    def read_data_info_consumer_not_monitor(self):
        vm_type = os.environ.get("VM_TYPE")
        path_file = self.working_dir + '/monitor_kafka' + '/' + vm_type.upper() + STORE_DATA_INFO_CONSUMER_NOT_MONITOR
        data = InitializeMonitorKafka.read_json_file(path_file)
        return data

    def write_info_consumer(self):
        data = self.read_data_info_consumer()

        try:
            if not data:
                return 0

            module_name = data.get('module_name')
            if not module_name:
                return 0
            else:
                module_name = module_name.lower()
            path_dir = APPLICATION_DATA_DIR + FOLDER_INFORMATION_CONSUMER_DATA_SHARE

            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

            path_dir = path_dir + FOLDER_INFORMATION_CONSUMER
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

            path_file = path_dir + '/{}.json'.format(module_name)
            with open(path_file, 'w') as f:
                f.write(json.dumps(data))

            print('Successfully write_info_consumer')
        except Exception as err:
            print(err)

    def write_info_consumer_not_monitor(self):
        data = self.read_data_info_consumer_not_monitor()
        try:
            if not data:
                return 0

            module_name = data.get('module_name')
            if not module_name:
                return 0
            else:
                module_name = module_name.lower()

            path_dir = APPLICATION_DATA_DIR + FOLDER_INFORMATION_CONSUMER_DATA_SHARE
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

            path_dir = path_dir + FOLDER_INFORMATION_CONSUMER_NOT_MONITOR
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)

            path_file = path_dir + '/{}.json'.format(module_name)
            with open(path_file, 'w') as f:
                f.write(json.dumps(data))

            print('Successfully write_info_consumer_not_monitor')
        except Exception as err:
            print(err)

    def start_process(self):
        self.write_info_consumer()
        self.write_info_consumer_not_monitor()
        print('successfully')


if __name__ == '__main__':
    InitializeMonitorKafka('MOBIO_TEMPLATE_HOME').write_info_consumer()
    InitializeMonitorKafka('MOBIO_TEMPLATE_HOME').write_info_consumer_not_monitor()
