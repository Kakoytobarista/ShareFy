class Assertions(object):

    @staticmethod
    def assert_are_equal(expected_result,
                         actual_result):
        assert expected_result == actual_result, (
            'Unexpected result value! Expected: {expected_result}. Actual: {actual_result}'.format(
                expected_result=expected_result, actual_result=actual_result))

    @staticmethod
    def assert_is_not_none(data):
        assert data is not None, ('Unexpected value in data, expected not None,'
                                  'data: {data}'.format(data=data))

    @staticmethod
    def assert_are_not_equal(expected_result,
                             actual_result):
        assert expected_result != actual_result, (
            'Unexpected result value! Expected: {expected_result}. Actual: {actual_result}'.format(
                expected_result=expected_result, actual_result=actual_result))

    @staticmethod
    def assert_value_is_not_empty(dictionary, key):
        if key not in dictionary:
            raise KeyError("Key: {key} not found in dictionary".format(key=key))
        if not dictionary[key]:
            raise ValueError("Value for key: {key} is empty".format(key=key))

    @staticmethod
    def assert_key_is_present(dictionary, key):
        if key not in dictionary:
            raise KeyError("Key: {key} not found in dictionary".format(key=key))

    @staticmethod
    def assert_dict_is_not_empty(dictionary):
        assert dictionary, "Dictionary: {dictionary} is empty".format(dictionary=dictionary)

    @staticmethod
    def assert_is_instance(first_obj, second_obj):
        assert isinstance(first_obj, second_obj), "Object {first_obj} is not an instance of {second_obj}".format(
            first_obj=first_obj, second_obj=second_obj
        )
