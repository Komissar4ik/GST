def strict_sequence_check(number_lists, current):
    # Проверяет строгую последовательность подразделов (например, 1.1, 1.2, 1.3 ...)
    same_level = [nums for nums in number_lists if len(nums) == len(current) and nums[:-1] == current[:-1]]
    if not same_level:
        return current[-1] == 1
    prev = max(same_level)
    return current[-1] == prev[-1] + 1