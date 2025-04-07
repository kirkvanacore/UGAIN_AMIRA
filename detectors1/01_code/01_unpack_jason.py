import os
import json
import csv

json_folder = 'detectors1/02_data/ugain_mar23sample_prealignment_asr'
csv_file = '/Users/kirkvanacore/Documents/PCLA_analyses/UGAIN_AMIRA/detectors1/02_data/speech_logs.csv'
csv_columns = ['file', 'version', 'timeRead', 'asr_model', 'full_text', 'word', 'confidence', 'start_time', 'end_time']

json_files = [f for f in os.listdir(json_folder) if f.lower().endswith('.json')]
if not json_files:
    print("No JSON files found in folder.")

with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    
    for json_file in json_files:
        file_path = os.path.join(json_folder, json_file)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
                continue

            version = data.get('version', '')
            timeRead = data.get('timeRead', '')
            asr_data = data.get('asr', {})

            if not asr_data:
                print(f"No asr data found in {json_file}")

            for asr_model, model_data in asr_data.items():
                if isinstance(model_data, dict) and 'data' in model_data:
                    full_text = model_data['data'].get('text', '')
                    transcription = model_data['data'].get('transcription', [])

                    if not transcription:
                        print(f"No transcription found in {json_file} for model {asr_model}")

                    for word_info in transcription:
                        writer.writerow({
                            'file': json_file,
                            'version': version,
                            'timeRead': timeRead,
                            'asr_model': asr_model,
                            'full_text': full_text,
                            'word': word_info.get('word', ''),
                            'confidence': word_info.get('confidence', ''),
                            'start_time': word_info.get('start_time', ''),
                            'end_time': word_info.get('end_time', '')
                        })

