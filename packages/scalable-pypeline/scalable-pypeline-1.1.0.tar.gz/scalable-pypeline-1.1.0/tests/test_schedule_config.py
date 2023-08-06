""" Tests confirming proper sermos.yaml formatting / parsing.
"""
import json
import pytest
from marshmallow.exceptions import ValidationError
from pypeline.schedule_config_schema import BaseScheduleSchema


class TestScheduleConfig:
    """ Test schemas in sermos/schedule_config_schema.py

    TODO Need to beef up tests.
    """
    valid_schedule = '/fixtures/api/demo_schedule_conf.json'
    invalid_dups = '/fixtures/api/demo_schedule_conf_invalid_dup_names.json'
    invalid_entries = '/fixtures/api/demo_schedule_conf_invalid_entries.json'

    with open('tests' + valid_schedule, 'r') as f:
        valid_schedule = json.loads(f.read())
    with open('tests' + invalid_dups, 'r') as f:
        invalid_dups = json.loads(f.read())
    with open('tests' + invalid_entries, 'r') as f:
        invalid_entries = json.loads(f.read())
        invalid_list = invalid_entries['schedules']

    def test_valid_schedule(self):
        """ Verify proper loading of full schedule and an individual entry
        """
        schema = BaseScheduleSchema()
        for schedule in self.valid_schedule['data']['results']:
            result = schema.load(schedule)
            assert result is not None

    def test_invalid_strings(self):
        """ Verify we properly validate some string values.
        """
        with pytest.raises(ValidationError) as e:
            # First entry doesn't even have valid keys in the dictionary
            BaseScheduleSchema().load(self.invalid_list[0])

        # Each schedule entry in our invalid list is invalid for a different
        # key's validation. Loop over them and verify they are all indeed
        # validated and raise a validation error for that key
        fields = ('config', 'scheduleType', 'every', 'period', 'dayOfWeek',
                  'name', 'queue', 'task')
        for idx, field in enumerate(fields):
            with pytest.raises(ValidationError) as e:
                BaseScheduleSchema().load(self.invalid_list[idx + 1])
            assert field in str(e.value.messages)
