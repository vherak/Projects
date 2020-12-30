#ifndef PLAYER_H
#define PLAYER_H
#include <string> 
using namespace std;

// Player class: holds all the important details for a player such as below:
class Player {
private:
	string playerName;
	string playerDifficulty;
	int playerScore = 0 ;
	int playerWins = 0;
	int playerGamesPlayed = 0;

public:
	Player();
	Player(string name, string difficulty);
	string getName();
	string getDifficulty();
	void setName(string name);
	void setDifficulty(string difficulty);
	void setPlayerWins(int wins);
	void setPlayerGamesPlayed(int gamesPlayed);
	int getScore();
	int getPlayerWins();
	int getPlayerGamesPlayed();
	void setScore(int score);
};
#endif

