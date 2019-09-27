from rest_framework import serializers

from weixin.models import BirthDayRecord


class BirthDayRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthDayRecord
        fields = ('id', 'name', 'birth_day', 'group_name', 'is_lunar_calendar', 'open_id')
