def flatten_list(s):
    result = []
    for item in s:
        if isinstance(item, list):
            result.extend(flatten_list(item))  # recursive call
        else:
            result.append(item)
    return result

# Test
s = [1, 2, [3, [4, 5], 6], 6, 7]
flattened_list = flatten_list(s)
print(flattened_list)
