#include "Player.h"
#include <string> 
using namespace std;

// default constructor for the player class
Player :: Player(){}

// constructor of the player class
Player::Player(string name, string difficulty) {
	playerName = name;
	playerDifficulty = difficulty;
}

// gets the name of the playe
string Player::getName() {
	return playerName;
}

// gets the difficulty of the player
string Player::getDifficulty() {
	return playerDifficulty ;
}

// sets the number of games played
void Player::setPlayerGamesPlayed(int gamesPlayed) {
	playerGamesPlayed = gamesPlayed;
}

// gets the number of games played by the player so far
int Player::getPlayerGamesPlayed() {
	return playerGamesPlayed;
}

// sets the number of wins of the player
void Player::setPlayerWins(int wins) {
	playerWins = wins;
}

// sets the name of the player
void Player::setName(string name) {
	playerName = name;
}

// sets the difficulty that the player chose
void Player::setDifficulty(string difficulty) {
	playerDifficulty = difficulty;
}

// gets the wins of the player
int Player::getPlayerWins() {
	return playerWins;
}

// gets the players score
int Player::getScore() {
	return playerScore;
}

// sets the players score
void Player::setScore(int score) {
	playerScore = score;
}

