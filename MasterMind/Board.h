#ifndef BOARD_H
#define BOARD_H
#include <string> 
#include <vector>
#include <list>
#include <array>

using namespace std;

// Board class: Holds all the important details for a board
class Board {
private:
	int boardRows=0 ;
	int boardColumns=0;
	int round = 0;
	string boardString = "";
	vector<string> thisBoard;
	vector<string> guesses;


public:
	Board();
	Board(int rows, int columns);
	void initializeBoard();
	void initializeGuesses();
	void updateBoard(int row,string symbol);
	int getColumns();
	int getRows();
	vector<string> getThisBoard();
	void updateGuesses(int row,string guess);
	string printBoard();
	void resetBoard();
	int getRounds();
	string getGuess(int position);
	void updateRounds();
	void setRows(int rows);
	void setCol(int rows);

};
#endif