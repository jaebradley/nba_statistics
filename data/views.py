from data.view_sets import PositionViewSet, TeamViewSet, PlayerViewSet, GameViewSet, SeasonViewSet, GamePlayerBoxScoreViewSet

positions_list = PositionViewSet.as_view({
    'get': 'list_positions'
})

position_detail = PositionViewSet.as_view({
    'get': 'retrieve_position'
})

team_detail = TeamViewSet.as_view({
    'get': 'retrieve_team'
})

teams_list = TeamViewSet.as_view({
    'get': 'list_teams'
})

players_list = PlayerViewSet.as_view({
    'get': 'list_players'
})

player_detail = PlayerViewSet.as_view({
    'get': 'retrieve_player'
})

games_list = GameViewSet.as_view({
    'get': 'list_games'
})

game_detail = GameViewSet.as_view({
    'get': 'retrieve_game'
})

seasons_list = SeasonViewSet.as_view({
    'get': 'list_seasons'
})

season_detail = SeasonViewSet.as_view({
    'get': 'retrieve_season'
})

game_player_box_scores_list = GamePlayerBoxScoreViewSet.as_view({
    'get': 'list_game_player_box_scores'
})

game_player_box_score_detail = GamePlayerBoxScoreViewSet.as_view({
    'get': 'retrieve_game_player_box_score'
})