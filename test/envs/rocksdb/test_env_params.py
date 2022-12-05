import unittest

from sysgym import EnvParamsDict
from sysgym.envs.rocksdb.schema import RocksDB10Params


class TestEnvParameters(unittest.TestCase):
    def setUp(self) -> None:
        self.params_space = RocksDB10Params()
        self.env_param = EnvParamsDict(self.params_space)

    def test_space_get_update_reset(self):
        print(str(self.env_param))
        default_value = self.params_space.level0_file_num_compaction_trigger.default
        self.assertEqual(
            self.env_param["level0_file_num_compaction_trigger"],
            default_value,
            msg="Assert the default is set as value.",
        )

        new_value = 10
        self.env_param["level0_file_num_compaction_trigger"] = new_value
        self.assertEqual(
            self.env_param["level0_file_num_compaction_trigger"],
            new_value,
            msg="Assert the value is updated.",
        )

        self.env_param.reset()
        self.assertEqual(
            self.env_param["level0_file_num_compaction_trigger"],
            default_value,
            msg="Assert the value is reseted back to default.",
        )

        new_value = 50
        self.env_param["level0_file_num_compaction_trigger"] = new_value
        self.assertEqual(
            self.env_param["level0_file_num_compaction_trigger"],
            new_value,
            msg="Assert the value is updated again.",
        )

        del self.env_param["level0_file_num_compaction_trigger"]
        self.assertEqual(
            self.env_param["level0_file_num_compaction_trigger"],
            default_value,
            msg="Assert the value is reseted back to default with delete.",
        )

    def test_get_no_member(self):
        # assert equals to default
        self.assertRaises(KeyError, lambda: self.env_param["not_a_member"])

    def test_update_with_numpy(self):
        default_value = self.params_space.level0_file_num_compaction_trigger.default
        self.assertEqual(
            self.env_param["level0_file_num_compaction_trigger"],
            default_value,
            msg="Assert the default is set as value.",
        )
        # assert update

        new_values = self.env_param.as_numpy() + 2

        self.env_param.update_from_numpy(new_values)

        self.assertEqual(
            self.env_param["level0_file_num_compaction_trigger"],
            default_value + 2,
            msg="Assert the value has been updated once fed as numpy.",
        )

        self.assertEqual(
            self.env_param.as_numpy().tolist(),
            new_values.tolist(),
            msg="Assert all values have been updated once fed as numpy.",
        )


if __name__ == "__main__":
    unittest.main()
