def find_max_difference_pair(data):
    max_diff = 0
    largest_value = None
    smallest_value_before_largest = None

    for i in range(1, len(data)):
        current_diff = data[i] - min(data[:i])
        if current_diff > max_diff:
            max_diff = current_diff
            largest_value = data[i]
            smallest_value_before_largest = min(data[:i])
    data.remove(largest_value)
    data.remove(smallest_value_before_largest)

    return (max_diff)


def modified_tbn(data):
    ans=[]

    for _ in range(2):        
        ans.append(find_max_difference_pair(data))

    return sum(ans)



dam_values = [30.0, 140.0, 40.0, 125.0, 50.0, 35.0, 70.0, 45.0, 60.0, 55.0, 80.0, 65.0, 90.0, 75.0, 100.0, 85.0, 110.0, 95.0, 120.0, 105.0, 130.0, 115.0, 15.0, 25.0]

print(modified_tbn(dam_values))
# result = find_max_difference_pair(dam_values)
# print("Largest Value:", result[0])
# print("Smallest Value Before Largest:", result[1])
# print("Maximum Difference:", result[2])
# print("Dam Values after Removal:", dam_values)


# def find_max_difference_pair_two(data):
#     max_diff = 0
#     largest_value = None
#     smallest_value_before_largest = None

#     for i in range(1, len(data)):
#         current_diff = data[i] - min(data[:i])
#         if current_diff > max_diff:
#             max_diff = current_diff
#             largest_value = data[i]
#             smallest_value_before_largest = min(data[:i])

#     return largest_value, smallest_value_before_largest, max_diff

# result = find_max_difference_pair_two(dam_values)
# print("Largest Value:", result[0])
# print("Smallest Value Before Largest:", result[1])
# print("Maximum Difference:", result[2])
