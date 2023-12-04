import json
import uuid

def add_id_and_vector_to_json(json_data,begin_id):
    json_data_with_id_vector = []
    last_id = begin_id

    for entry in json_data:
        new_id = str(uuid.uuid4())
        entry_with_id_vector = {
            "id": new_id,
            "values": entry["vector_field"],
            "metadata" : {
                "text": entry["text"],
                "source": entry["metadata"]["source"],
                "title": entry["metadata"]["title"],
                "created_at": entry["metadata"]["created_at"],
                "start_index": entry["metadata"]["start_index"]
             }
        }
        json_data_with_id_vector.append(entry_with_id_vector)
        last_id = new_id

    # Print the last ID in the console
    print("Last ID:", last_id)

    return json_data_with_id_vector,last_id

def split_and_save_data(file_index, data, num_parts=8):
    part_size = len(data) // num_parts
    for i in range(num_parts):
        start_index = i * part_size
        end_index = (i + 1) * part_size if i < num_parts - 1 else None
        part_data = data[start_index:end_index]

        with open(f'json_part_{file_index}_{i+1}.json', 'w') as file:
            json.dump(part_data, file, indent=2)

def main():
    for i in range(0,10):
        # Load JSON data from file
        with open(f'swisscom_webpage_{i}.json', 'r') as file:
            original_data = json.load(file)

        # Add "id" and "vector" fields to each entry
        if i == 0:
            data_with_id_vector, last_id_returned = add_id_and_vector_to_json(original_data, None)
        else: data_with_id_vector, last_id_returned = add_id_and_vector_to_json(original_data, last_id_returned)

        # Save data with "id" and "vector" fields to a new JSON file
        with open('json_with_id_vector.json', 'w') as file:
            json.dump(data_with_id_vector, file, indent=2)

        # Split the data into four parts and save each part to a separate JSON file
        split_and_save_data(i, data_with_id_vector, num_parts=8)

if __name__ == "__main__":
    main()
