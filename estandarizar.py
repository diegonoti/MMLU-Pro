import pandas as pd
import json

# Load the datasets
validation_historia_del_peru = pd.read_csv('C:/Users/diego/OneDrive/Escritorio/MMLU-Pro/data/validation/Updated_Standardized_Validation_Historia_del_Peru.csv')
test_historia_del_peru = pd.read_csv('C:/Users/diego/OneDrive/Escritorio/MMLU-Pro/data/test/Updated_Standardized_Test_Historia_del_Peru.csv')

# Function to check if options are properly formatted
def check_options_format(options_str):
    try:
        options = json.loads(options_str)
        return isinstance(options, list)
    except json.JSONDecodeError:
        return False

# Check the format of the options column in both datasets
validation_historia_del_peru['options_formatted'] = validation_historia_del_peru['options'].apply(check_options_format)
test_historia_del_peru['options_formatted'] = test_historia_del_peru['options'].apply(check_options_format)

# Display rows with incorrectly formatted options
print("Validation set - Incorrectly formatted options:")
print(validation_historia_del_peru[~validation_historia_del_peru['options_formatted']])

print("\nTest set - Incorrectly formatted options:")
print(test_historia_del_peru[~test_historia_del_peru['options_formatted']])

# Correct any issues with options formatting
def reformat_options(options_str):
    if not check_options_format(options_str):
        options_list = options_str.split(';')
        options_list = [option.strip()[3:].strip() for option in options_list]  # Remove "A) ", "B) ", etc.
        return json.dumps(options_list)
    return options_str

validation_historia_del_peru['options'] = validation_historia_del_peru['options'].apply(reformat_options)
test_historia_del_peru['options'] = test_historia_del_peru['options'].apply(reformat_options)

# Remove the temporary 'options_formatted' column
validation_historia_del_peru.drop(columns=['options_formatted'], inplace=True)
test_historia_del_peru.drop(columns=['options_formatted'], inplace=True)

# Save the corrected datasets
validation_historia_del_peru.to_csv('C:/Users/diego/OneDrive/Escritorio/MMLU-Pro/data/validation/Corrected_Standardized_Validation_Historia_del_Peru.csv', index=False)
test_historia_del_peru.to_csv('C:/Users/diego/OneDrive/Escritorio/MMLU-Pro/data/test/Corrected_Standardized_Test_Historia_del_Peru.csv', index=False)

print("Datasets corrected and saved successfully.")
