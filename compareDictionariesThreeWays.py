def compare_dicts2(dict1, dict2, result_matrix, parent_key=''):
    for key in dict1:
        full_key = parent_key + '.' + key if parent_key else key
        
        if isinstance(dict1[key], dict) and isinstance(dict2.get(key, None), dict):
            compare_dicts2(dict1[key], dict2[key], result_matrix, full_key)  # Recursively compare nested dictionaries
        elif dict1[key] is not None and dict2.get(key, None) is not None:
            value1 = dict1[key]
            value2 = dict2[key]
            
            if value1 == value2:
                print(f"Key '{full_key}' has the same value in both dictionaries:", value1)
            else:
                print(f"Key '{full_key}' has different values:")
                print(f"  Value in dict1: {value1}")
                print(f"  Value in dict2: {value2}")
                
            result_matrix.append([full_key, value1, value2])
            print("result matrix is ", result_matrix)

def compare_dicts3(dict1, dict2, result_matrix):
    keyPosition = 0
    for key in dict1:
        if key in dict2 and dict1[key] is not None and dict2[key] is not None:
            value1 = dict1[key]
            value2 = dict2[key]
            
            if isinstance(value1, dict) and isinstance(value2, dict):
                compare_dicts2(value1, value2, result_matrix)  # Recursively compare nested dictionaries
            elif value1 == value2:
                print(f"Key '{key}' has the same value in both dictionaries:", value1)
            else:
                print(f"Key '{key}' has different values:")
                print(f"  Value in dict1: {value1}")
                print(f"  Value in dict2: {value2}")
                
            result_matrix.append([key, value1, value2])
            keyPosition = keyPosition + 1

    return result_matrix

# We're gonna have this return a 2D array: each value in the first dimension will represent a key value pair.
# The second dimension is the key value pair and the name of that node. Example:
# [ ["tempCpu", "33", ">=33"], ["humidity", "22.9", "<38.3"]  ]
def compare_dicts(dict1, dict2, result_matrix):
  keyPosition = 0
  for key in dict1:
    if key in dict2:
      
      value1 = dict1[key]
      value2 = dict2[key]
      
      if isinstance(value1, dict) and isinstance(value2, dict):
        compare_dicts(value1, value2, result_matrix)  # Recursively compare nested dictionaries
      elif value1 == value2:
        print(f"Key '{key}' has the same value in both dictionaries:", value1)
      else:
        print(f"Key '{key}' has different values:")
        print(f"  Value in dict1: {value1}")
        print(f"  Value in dict2: {value2}")
        
      result_matrix.append([key, value1, value2])
      keyPosition = keyPosition + 1
  
  return result_matrix
