import json
from datetime import datetime


def save_dict_to_file(d: dict, file_path: str) -> None:
    try:
        with open(file_path, 'w') as _file:
            _file.write(json.dumps(d))
        print(f"Saving dict data within '{file_path}")
    except Exception as e:
        print(f"Exception '{e}' on saving Data to '{file_path}'")


class Recorder(object):
    def __init__(self):
        self.buffer = []

    def end_recording(self, file_path, slate_data, calib_point):
        print("Ending Recording...")
        print(f"\tSample Count: {len(self.buffer)} | "
              f"Length: {round(self.buffer[-1]['time']-self.buffer[0]['time'], 2)} seconds | "
              f"Avg: {len(self.buffer)/round(self.buffer[-1]['time']-self.buffer[0]['time'], 2)} samples per second")

        recorded_data = dict()
        recorded_data['name'] = f"{slate_data[0]}.{slate_data[1]}.tk{slate_data[2]}"
        recorded_data['slate'] = slate_data[0]
        recorded_data['setup'] = slate_data[1]
        recorded_data['take'] = int(slate_data[2])
        recorded_data['date'] = str(datetime.now())
        recorded_data['start_time'] = str(self.buffer[0]['time'])
        recorded_data['end_time'] = str(self.buffer[-1]['time'])
        recorded_data['calib_point'] = calib_point
        recorded_data['samples_count'] = len(self.buffer)
        recorded_data['samples'] = dict()
        for sample in self.buffer:
            t = sample['time']-self.buffer[0]['time']
            recorded_data['samples'][str(t)] = sample.get('tracker_1')

        # Save to file
        now = datetime.now()
        today = datetime.today()
        path = f"{file_path}/{today.year}{str(today.month).zfill(2)}" \
               f"{str(today.day).zfill(2)}_" \
               f"{str(now.hour).zfill(2)}{str(now.minute).zfill(2)}{str(now.second).zfill(2)}_" \
               f"{recorded_data['name']}.json"

        print(f"\tSaving recorded data:\t{path}")
        save_dict_to_file(recorded_data, path)

        self.buffer = []

    def add_sample(self, sample):
        self.buffer.append(sample)
