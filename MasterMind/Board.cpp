#include "Board.h"
#include <string> 
#include <vector>
#include <array>
#include <iostream>
#include <string>
#include <typeinfo>


using namespace std;

// default constructor for the board class
Board::Board() {
	boardRows = 0;
	boardColumns = 0;
	round = 0;
}

// board constructor
Board::Board(int rows, int columns) {
	boardRows = rows;
	boardColumns = columns;
}

// initializes the board
void Board::initializeBoard() {
	for (int i = 0; i < boardRows; i++) {
		thisBoard.push_back("_ _ _ _");
	}
}

// initializes the guesses
void Board::initializeGuesses() {
	for (int i = 0; i < boardRows; i++) {
		guesses.push_back("_ _ _ _");
	}
}

// updates the guesses of player after every round with the feedback symbols
void Board::updateGuesses(int row, string guess) {
	guesses[round] = guess;
}

// updates the board after every round with player input
void Board::updateBoard(int row,string userInput) {
	thisBoard[round] = userInput;
}

// returns the columns of the board
int Board::getColumns() {
	return boardColumns;
}

// returns the rows of the board
int Board::getRows() {
	return boardRows;
}

// returns the rounds
int Board::getRounds() {
	return round;
}

// updates the rounds of the game
void Board::updateRounds() {
	round += 1;
}

// gets the players guess at this position
string Board::getGuess(int pos) {
	return thisBoard[pos];
}

// returns the board
vector<string> Board::getThisBoard() {
	return thisBoard;
}

// prints the board nicely
string Board::printBoard() {
	string symbolsString = guesses[round];
	string userInput = thisBoard[round];
	string x = "";
	string boxTop = "";
	string boxMid = "";
	string boxBot = "";
	for (int num = 0; num < boardColumns; num++) {
		x = userInput[num];
		boxTop += " .---. ";
		boxMid += " | " + x + " | " ;
		boxBot += " '---' ";
	}	
	boardString += boxTop + "\n" + boxMid + "\n" + boxBot;
	
	for (int i = 0; i < boardColumns; i++) {
		x = symbolsString[i];
		boardString += x + " "; 
	}
	boardString += "\n";
	return boardString;
}

// resets the variables of the board
void Board::resetBoard() {
	round = 0;
	boardRows = 0;
	boardColumns = 0;
	boardString = "";
	vector<string> thisBoard;
	vector<string> guesses;
}

// sets the rows of the board
void Board::setRows(int rows) {
	boardRows = rows;
}

// sets the columns of the board
void Board::setCol(int col) {
	boardColumns = col;
}










