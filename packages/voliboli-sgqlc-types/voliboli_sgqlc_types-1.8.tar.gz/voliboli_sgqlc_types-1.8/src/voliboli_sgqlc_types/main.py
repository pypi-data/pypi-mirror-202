from sgqlc.types import String, Type, Field, ID, Boolean, list_of
from sgqlc.operation import Operation

class Player(Type):
    name = String
    teamName = String
    votes = String
    totalPoints = String
    breakPoints = String
    winloss = String
    totalServe = String
    errorServe = String
    pointsServe = String
    totalReception = String
    errorReception = String
    posReception = String
    excReception = String
    totalAttacks = String
    errorAttacks = String
    blockedAttacks = String
    pointsAttack = String
    posAttack = String
    pointsBlock = String
    dateTeam = String

class PlayerResult(Type):
    success = Boolean
    errors =  list_of(String)
    player = Player

class PlayersResult(Type):
    success = Boolean
    errors = list_of(String)
    players = list_of(Player)

class Team(Type):
    name = String
    players = list_of(Player)

class TeamResult(Type):
    success = Boolean
    errors = list_of(String)
    team = Team

class TeamsResult(Type):
    success = Boolean
    errors = list_of(String)
    teams = list_of(Team)

class Query(Type):
    getTeam = Field(TeamResult, args={'name': String})
    getTeams = Field(TeamsResult)
    getPlayer = Field(PlayerResult, args={'name': String})
    getPlayers = Field(PlayersResult)

class Mutation(Type):
    createTeam = Field(TeamResult, args={'name': String})
    deleteTeam = Field(TeamResult, args={'name': String})
    createPlayer = Field(PlayerResult, args={'name': String, 'teamName': String})
    updatePlayer = Field(PlayerResult, args={'name': String,
                                             'votes': String, 
                                             'totalPoints': String,
                                             'breakPoints': String,
                                             'winloss': String,
                                             'totalServe': String,
                                             'errorServe': String,
                                             'pointsServe': String,
                                             'totalReception': String,
                                             'errorReception': String,
                                             'posReception': String,
                                             'excReception': String,
                                             'totalAttacks': String,
                                             'errorAttacks': String,
                                             'blockedAttacks': String,
                                             'pointsAttack': String,
                                             'posAttack': String,
                                             'pointsBlock': String,
                                             'dateTeam': String})
    deletePlayer = Field(PlayerResult, args={'name': String})