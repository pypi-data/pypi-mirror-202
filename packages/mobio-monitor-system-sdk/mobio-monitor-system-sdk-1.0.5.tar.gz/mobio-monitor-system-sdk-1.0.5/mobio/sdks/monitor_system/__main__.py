import sys

from initialize_monitor_kafka import InitializeMonitorKafka

if __name__ == '__main__':
    name_space = sys.argv[1]
    print(name_space)
    InitializeMonitorKafka(name_space).write_info_consumer()
    InitializeMonitorKafka(name_space).write_info_consumer_not_monitor()
