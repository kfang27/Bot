unit_names_input = input("Enter the names of your units in order: ").strip().lower()
    
if not unit_names_input:
    print("No unit names provided.")
    
unit_names = []
for name in unit_names_input.split(','):
    stripped_name = name.strip()
    # checks if it's an empty string now because the strip() before, removes any trailing whitespace, including strings such as ' '
    if stripped_name:
        split_result = stripped_name.split()
        for i in split_result:
            unit_names.append(i.capitalize())

print(unit_names)