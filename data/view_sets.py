# Create your views here.

from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from data.models import Team, Position, Season, Player, Game, GamePlayerBoxScore
from data.serializers import TeamSerializer, PositionSerializer, SeasonSerializer, PlayerSerializer, GameSerializer, \
    GamePlayerBoxScoreSerializer


class QuerySetReadOnlyViewSet(ReadOnlyModelViewSet):
    def build_response(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PositionViewSet(QuerySetReadOnlyViewSet):
    serializer_class = PositionSerializer
    queryset = Position.objects.all().order_by('name')

    def list_positions(self, request, *args, **kwargs):
        return self.build_response(queryset=self.get_queryset())

    def retrieve_position(self, request, *args, **kwargs):
        result = self.queryset.filter(position__id=kwargs.get('position_id'))
        return self.build_response(queryset=result)


class TeamViewSet(QuerySetReadOnlyViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all().order_by('name')

    def list_teams(self, request, *args, **kwargs):
        return self.build_response(queryset=self.get_queryset())

    def retrieve_team(self, request, *args, **kwargs):
        result = self.queryset.filter(id=kwargs.get('team_id'))
        return self.build_response(queryset=result)


class SeasonViewSet(QuerySetReadOnlyViewSet):
    serializer_class = SeasonSerializer
    queryset = Season.objects.all().order_by('start_time', 'end_time')

    def list_seasons(self, request, *args, **kwargs):
        return self.build_response(queryset=self.get_queryset())

    def retrieve_team(self, request, *args, **kwargs):
        result = self.get_queryset()
        if 'team_id' in kwargs:
            result = result.filter(id=kwargs.get('team_id'))

        return self.build_response(queryset=result)


class PlayerViewSet(QuerySetReadOnlyViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.all().order_by('name')

    def list_players(self, request, *args, **kwargs):
        result = self.get_queryset()
        if 'source_id' in kwargs:
            result = result.filter(source_id=kwargs.get('source_id'))

        return self.build_response(queryset=result)

    def retrieve_player(self, request, *args, **kwargs):
        result = self.queryset.filter(id=kwargs.get('player_id'))
        return self.build_response(queryset=result)


class GameViewSet(QuerySetReadOnlyViewSet):
    serializer_class = GameSerializer
    queryset = Game.objects.all().order_by('start_time')

    def list_games(self, request, *args, **kwargs):
        return self.build_response(queryset=self.get_queryset())

    def retrieve_game(self, request, *args, **kwargs):
        result = self.queryset.filter(id=kwargs.get('game_id'))

        return self.build_response(queryset=result)


class GamePlayerBoxScoreViewSet(QuerySetReadOnlyViewSet):
    serializer_class = GamePlayerBoxScoreSerializer
    queryset = GamePlayerBoxScore.objects.all().order_by('game__start_time')

    def list_game_player_box_scores(self, request, *args, **kwargs):
        return self.build_response(queryset=self.get_queryset())

    def retrieve_game_player_box_score(self, request, *args, **kwargs):
        result = self.queryset.filter(id=kwargs.get('game_player_box_score_id'))
        return self.build_response(queryset=result)
