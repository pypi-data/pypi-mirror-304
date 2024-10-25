from playbracket.models import Player, Sport, Event, League, Match
from rest_framework import serializers


class ChoiceField(serializers.ChoiceField):

    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return self._choices[str(obj.pk)]

    def to_internal_value(self, data):
        if data not in self._choices.keys():
            self.fail("invalid_choice", input=data)
        return Sport.objects.get(pk=data)


class MultipleChoiceField(serializers.MultipleChoiceField):

    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return obj.instance.sports.all().values_list('name', flat=True)

    def to_internal_value(self, data):
        if not [True for key in data if key in self._choices.keys()]:
            self.fail("invalid_choice", input=data)
        return Sport.objects.filter(pk__in=data)


class PlayerSerializer(serializers.ModelSerializer):
    sports = MultipleChoiceField(choices=[(str(s.pk), s.name) for s in Sport.objects.all()])

    class Meta:
        model = Player
        fields = "__all__"


class SportSerializer(serializers.ModelSerializer):
    players = serializers.ListField(source="players_display", required=False)

    class Meta:
        model = Sport
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    matches = serializers.ListField(source="matches_display", required=False, read_only=True)
    players = serializers.ListField(source="players_display", required=False, read_only=True)

    class Meta:
        model = Event
        fields = "__all__"


class LeagueSerializer(serializers.ModelSerializer):
    sport = ChoiceField(choices=[(str(s.pk), s.name) for s in Sport.objects.all()])

    class Meta:
        model = League
        fields = "__all__"


class MatchSerializer(serializers.ModelSerializer):
    winners_display = serializers.ListField(read_only=True)
    winners = serializers.MultipleChoiceField(choices=[p for p in Player.objects.all()])
    losers_display = serializers.ListField(read_only=True)
    losers = serializers.MultipleChoiceField(choices=[p for p in Player.objects.all()])
    league_display = serializers.CharField(source="league.name", read_only=True)
    event_display = serializers.CharField(source="event.__str__", read_only=True)

    class Meta:
        model = Match
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)
