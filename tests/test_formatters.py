import unittest

from drf_logger.formatters import JSONExtraFormatter


class JSONExtraFormatterTests(unittest.TestCase):

    def test_json_dict_to_string_simple(self):
        dic: dict = {'key': 'hey'}
        formatter = JSONExtraFormatter()
        dict_str = formatter._dict_to_string(dic)
        self.assertEqual(dict_str, '{"key": "hey"}')

    def test_encode_japanese(self):
        """ Set json.dumps(, ensure_ascii=True), it causes text garbling
            in Japanese.
        """
        dic: dict = {'key': 'キー'}
        formatter = JSONExtraFormatter()
        dict_str = formatter._dict_to_string(dic)

        self.assertEqual(dict_str, '{"key": "キー"}')
