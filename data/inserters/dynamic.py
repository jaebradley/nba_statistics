# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import logging.config
import os

from nba_data import Client as NbaClient, Season as NbaSeason, DateRange as NbaDateRange

from data.models import Team as TeamModel, Season as SeasonModel, Player as PlayerModel, \
    Game as GameModel, GamePlayerBoxScore as NbaGamePlayerBoxScoreModel

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), '../../logging.conf'))
logger = logging.getLogger('inserter')

# TODO: @jbradley refactor all of this ASAP


class NbaPlayersInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Inserting NBA players')
        for season in SeasonModel.objects.order_by('start_time'):
            logger.info('Fetching players from NBA API for season: %s' % season)
            query_season = NbaSeason.get_season_by_start_and_end_year(start_year=season.start_time.year,
                                                                      end_year=season.end_time.year)
            for player in NbaClient.get_players(season=query_season):
                logger.info('Player: %s' % player.__dict__)
                player_model_object, created = PlayerModel.objects.get_or_create(name=player.name.strip(),
                                                                                 source_id=player.player_id)
                logger.info('Created: %s | Player: %s', created, player_model_object)


class NbaGamesInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        logger.info('Insert NBA games')
        for season in SeasonModel.objects.order_by('start_time'):
            logger.info('Season: %s' % season)
            game_counts = NbaClient.get_game_counts_in_date_range(NbaDateRange(start=season.start_time.date(),
                                                                               end=season.end_time.date()))
            for date_value, game_count in game_counts.items():
                logger.info('%s games on %s', game_count, date_value)
                for game in NbaClient.get_games_for_date(date_value=date_value):
                    logger.info('Inserting game: %s' % game.__dict__)
                    # TODO: @jbradley deal with All Star game
                    if game.matchup.home_team is not None and game.matchup.away_team is not None:
                        logger.info('Game Id: %s' % game.game_id)
                        logger.info('Home Team: %s vs. Away Team: %s @ %s',
                                    game.matchup.home_team, game.matchup.away_team, game.start_time)
                        home_team = TeamModel.objects.get(name=game.matchup.home_team.value)
                        away_team = TeamModel.objects.get(name=game.matchup.away_team.value)
                        game, created = GameModel.objects.get_or_create(home_team=home_team,
                                                                        away_team=away_team,
                                                                        season=season,
                                                                        start_time=game.start_time,
                                                                        source_id=game.game_id)
                        logger.info('Created: %s | Game: %s', created, game)


class NbaBoxScoreInserter:

    def __init__(self):
        pass

    @staticmethod
    def insert():
        for season in SeasonModel.objects.order_by('start_time'):
            for game in GameModel.objects.filter(start_time__lte=season.end_time).filter(start_time__gte=season.start_time):
                logger.info('Getting traditional box score for: %s', game.source_id)
                traditional_box_score = NbaClient.get_traditional_box_score(game_id=str(game.source_id))
                for player_box_score in traditional_box_score.player_box_scores:
                    logger.info(player_box_score.player.__dict__)
                    player, created = PlayerModel.objects.get_or_create(name=player_box_score.player.name, source_id=player_box_score.player.id)
                    logger.info('Created: %s | Player: %s', created, player)

                    box_score, created = NbaGamePlayerBoxScoreModel.objects.get_or_create(
                            game=game, player=player, status=player_box_score.player.status.type.value,
                            explanation=player_box_score.player.status.comment,
                            seconds_played=player_box_score.seconds_played,
                            field_goals_made=player_box_score.field_goals_made,
                            field_goals_attempted=player_box_score.field_goal_attempts,
                            three_point_field_goals_made=player_box_score.three_point_field_goals_made,
                            three_point_field_goals_attempted=player_box_score.three_point_field_goal_attempts,
                            free_throws_made=player_box_score.free_throws_made,
                            free_throws_attempted=player_box_score.free_throw_attempts,
                            offensive_rebounds=player_box_score.offensive_rebounds,
                            defensive_rebounds=player_box_score.defensive_rebounds,
                            assists=player_box_score.assists, steals=player_box_score.steals,
                            blocks=player_box_score.blocks, turnovers=player_box_score.turnovers,
                            personal_fouls=player_box_score.personal_fouls,
                            plus_minus=player_box_score.plus_minus)
                    logger.info('Created: %s | Box Score: %s', created, box_score)
