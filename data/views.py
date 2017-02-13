from data.view_sets import PositionViewSet, TeamViewSet, PlayerViewSet, GameViewSet, SeasonViewSet, GamePlayerBoxScoreViewSet

positions_list = PositionViewSet.as_view({
    'get': 'list'
})

position_detail = PositionViewSet.as_view({
    'get': 'retrieve'
})

teams_list = TeamViewSet.as_view({
    'get': 'list'
})

team_detail = TeamViewSet.as_view({
    'get': 'retrieve'
})

players_list = PlayerViewSet.as_view({
    'get': 'list'
})

player_detail = PlayerViewSet.as_view({
    'get': 'retrieve'
})

games_list = GameViewSet.as_view({
    'get': 'list'
})

game_detail = GameViewSet.as_view({
    'get': 'retrieve'
})

seasons_list = SeasonViewSet.as_view({
    'get': 'list'
})

season_detail = SeasonViewSet.as_view({
    'get': 'retrieve'
})

game_player_box_scores_list = GamePlayerBoxScoreViewSet.as_view({
    'get': 'list'
})

game_player_box_score_detail = GamePlayerBoxScoreViewSet.as_view({
    'get': 'retrieve'
})