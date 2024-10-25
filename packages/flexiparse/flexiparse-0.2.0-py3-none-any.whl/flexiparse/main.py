import json
import pandas as pd
import sys

# Function to extract field mappings from the request file
def extract_field_mappings_from_request(request_data):
    aggs_info = {}  # key: { 'field_name': ..., 'agg_type': ..., 'path': ... }
    field_order = []
    contains_sms = False  # Flag to indicate if SMS-related fields are present

    def recursive_extract(aggs, path=[]):
        nonlocal contains_sms
        for key, value in aggs.items():
            if 'terms' in value:
                field_name = value['terms']['field']
                if 'sms' in field_name.lower():
                    contains_sms = True
                aggs_info[key] = {
                    'field_name': field_name,
                    'agg_type': 'terms',
                    'path': path + [key]
                }
                field_order.append(key)
            elif any(metric in value for metric in ['sum', 'count', 'avg', 'max', 'min', 'value_count']):
                metric_type = next(metric for metric in ['sum', 'count', 'avg', 'max', 'min', 'value_count'] if metric in value)
                field_name = value[metric_type].get('field', key)  # Some metrics like 'count' may not have a field
                if 'sms' in field_name.lower():
                    contains_sms = True
                aggs_info[key] = {
                    'field_name': field_name,
                    'agg_type': metric_type,
                    'path': path + [key]
                }
                field_order.append(key)
            elif 'date_histogram' in value:
                field_name = value['date_histogram']['field']
                aggs_info[key] = {
                    'field_name': field_name,
                    'agg_type': 'date_histogram',
                    'path': path + [key]
                }
                field_order.append(key)
            if 'aggs' in value:
                recursive_extract(value['aggs'], path + [key])

    recursive_extract(request_data['aggs'])
    return aggs_info, field_order, contains_sms

# Helper function to extract simplified field names
def extract_field_name(field):
    # Remove '.keyword' or similar suffixes
    if '.' in field:
        field = field.split('.')[0]
    # Extract the last part after '_'
    field_parts = field.split('_')
    field_name = field_parts[-1]
    return field_name

# Recursive function to parse response buckets dynamically
def parse_buckets(buckets, parent_data=None, current_aggs_key=None, aggs_info=None, level=0, is_sms=False):
    rows = []
    for bucket in buckets:
        row = parent_data.copy() if parent_data else {}

        # Get the current aggregation info
        agg_info = aggs_info.get(current_aggs_key, {})
        field_name_full = agg_info.get('field_name')
        agg_type = agg_info.get('agg_type')

        if field_name_full:
            field_name = extract_field_name(field_name_full)
            if agg_type == 'date_histogram':
                # Convert date from epoch to datetime and extract only the date part
                date_str = bucket.get('key_as_string')
                row['date'] = pd.to_datetime(date_str).strftime('%Y-%m-%d')
            elif agg_type == 'terms':
                row[field_name] = bucket.get('key')
            elif agg_type in ['sum', 'count', 'avg', 'max', 'min', 'value_count']:
                metric_value = bucket.get(agg_info['agg_type'])
                if isinstance(metric_value, dict) and 'value' in metric_value:
                    row[field_name] = metric_value['value']
                elif isinstance(metric_value, (int, float)):
                    row[field_name] = metric_value

        # Process metric aggregations in this bucket
        for key in bucket:
            if key in aggs_info:
                sub_agg_info = aggs_info[key]
                sub_field_name_full = sub_agg_info['field_name']
                sub_field_name = extract_field_name(sub_field_name_full)
                sub_agg_type = sub_agg_info['agg_type']
                if sub_agg_type in ['sum', 'count', 'avg', 'max', 'min', 'value_count']:
                    metric_value = bucket.get(key)
                    if isinstance(metric_value, dict) and 'value' in metric_value:
                        row[sub_field_name] = metric_value['value']
                    elif isinstance(metric_value, (int, float)):
                        row[sub_field_name] = metric_value

        # Process sub-aggregations
        sub_aggs_present = False
        for key in bucket:
            if key in aggs_info and 'buckets' in bucket[key]:
                sub_aggs_present = True
                rows += parse_buckets(
                    bucket[key]['buckets'],
                    parent_data=row,
                    current_aggs_key=key,
                    aggs_info=aggs_info,
                    level=level + 1,
                    is_sms=is_sms
                )

        # If no further sub-aggregations, we're at the leaf level
        if not sub_aggs_present:
            # Assign 'doc_count' as 'smsCount' if processing SMS data
            if is_sms:
                row['smsCount'] = bucket.get('doc_count', 0)
            rows.append(row)
    return rows

# Function to parse and process the data
def process_data(request_file, response_file, output_csv):
    # Load the JSON data from the request file
    with open(request_file, 'r') as f:
        request_data = json.load(f)

    # Extract field mappings from the request file
    aggs_info, field_order, contains_sms = extract_field_mappings_from_request(request_data)

    # Load the JSON data from the response file
    with open(response_file, 'r') as f:
        response_data = json.load(f)

    # Find the top-level aggregation key
    top_level_key = next(iter(response_data['aggregations']))
    top_level_buckets = response_data['aggregations'][top_level_key]['buckets']

    # Parse the buckets dynamically, passing the SMS flag
    parsed_data = parse_buckets(
        top_level_buckets,
        current_aggs_key=top_level_key,
        aggs_info=aggs_info,
        is_sms=contains_sms
    )

    # Create a DataFrame from the parsed data
    df = pd.DataFrame(parsed_data)

    # Build priority_fields based on field_order
    priority_fields = []
    for key in field_order:
        field_name_full = aggs_info[key]['field_name']
        field_name = extract_field_name(field_name_full)
        if aggs_info[key]['agg_type'] == 'date_histogram':
            field_name = 'date'
        if field_name not in priority_fields:
            priority_fields.append(field_name)

    # Remove duplicates while preserving order
    def remove_duplicates(seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    priority_fields = remove_duplicates(priority_fields)

    # Include 'smsCount' if it exists and SMS data is being processed
    if contains_sms and 'smsCount' in df.columns and 'smsCount' not in priority_fields:
        priority_fields.append('smsCount')

    # Exclude 'doc_count' if present
    if 'doc_count' in df.columns:
        df = df.drop(columns=['doc_count'])

    # Hardcoded check to rename '0' to 'callingParty' for voice output
    if '0' in df.columns:
        df = df.rename(columns={'0': 'callingParty'})

    # Reorder the DataFrame columns based on your requirements
    available_columns = list(df.columns)

    # Define the volume columns to move to the end
    volume_columns = ['downlinkVolume', 'uplinkVolume', 'totalVolume']

    # Identify new metric columns (e.g., 'duration') excluding 'smsCount'
    metric_columns = [col for col in available_columns if col not in priority_fields + volume_columns + ['smsCount']]

    # Remove volume and metric columns from available_columns
    base_columns = [col for col in available_columns if col not in volume_columns + metric_columns + ['smsCount']]

    # Now, reorder base columns as per priority_fields
    ordered_columns = [col for col in priority_fields if col in base_columns]
    remaining_columns = [col for col in base_columns if col not in ordered_columns]
    ordered_columns += remaining_columns

    # Append 'smsCount' if present and SMS data is being processed
    if contains_sms and 'smsCount' in available_columns:
        ordered_columns.append('smsCount')

    # Append the metric columns
    ordered_columns += metric_columns

    # Append the volume columns, sorted alphabetically
    ordered_columns += sorted([col for col in volume_columns if col in available_columns])

    # Reorder the DataFrame
    df = df[ordered_columns]

    # Export to CSV
    df.to_csv(output_csv, index=False)

    return df

# Optional: Separate function to display the DataFrame
def display_dataframe(df):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(df)
