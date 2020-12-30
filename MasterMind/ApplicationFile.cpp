/**************************************************
 Project: Assignment 3
 Author: Vhera Kaey Vijayaraj 28903013
 Purpose: Master Mind :: Space Ranger
**************************************************/
//NOTE:
// All the ascii art used in this game are from the websites: https ://www.asciiart.eu/space and http: //www.oocities.org/spunk1111/haloween.htm
// All text files are written by myself.
// EXTRA FEATURES:
// 1) Theme: The game has a space theme
// 2) Player can select a skill level: Space Cadet, Cosmic Commander or Galactic Hero
// 3) Scoring system
// 4) Player has additional options: getting a hint/ resigning the game
// 5) Allows player to select what elements they want to use in the game

#include "Player.h"
#include "Board.h"
#include <iostream>
#include <typeinfo>
#include <string>
#include <fstream>
#include <ctime>
#include <vector>
#include <list>
using namespace std;



//declaring all the functions used
void playGame();
void getPlayerDetails(Player* player, Board* board, string &level,string &elements);
void printFile(string filename);
void gameOver(Player* player);
bool quitMission(Player* playerName);
void displayScore(Player* player, Board* board);
void getElementsAndDifficulty(Player* player, Board* board, string& level, string& elements);
void generateSecretCode(string& code, Board* board,string &elements);
bool isLetterInString(char letter, string &aString);
bool resignMission(string secretCode, Player* player);
string getSymbolRep(string guess, string secretCode);
bool restartGame(Board* board, Player* player, string& secretCode, string& elements, bool& hasUsedHint, string& level);
void getHint(string code,bool &hasUsedHint);
bool isCodeBroken(string code, string guess);
void makeGuess(Board* board, string secretCode);


int main() {
	// Runs the function playGame() which runs the whole game
	playGame();
	system("pause");
	return 0;
}

void playGame() {
	// declaring all the variables used
	string level;
	string elements;
	bool hasUsedHint = false;
	string secretCode;

	// Added a list to "talk" to the player after each round
	vector<string> talkingList = { "Master Kaiju:*YAWN* You're seriously BORING ME",
								  "Master Kaiju: This is going to take forever, isn't it?",
								  "Master Kaiju: PUKA PUKA PUKA! I...don't know why I said that..",
								  "Master Kaiju: Tick Tock goes the clock! MUAHAHHHAHAHHAHHAH *cough cough*..Ok that laugh was too much.." ,
								  "Zhu: Psst you can do this, space Ranger!",
								  "Zhu: Just keep doing your best!",
								  "Zhu: Bzz Bzz Does anyone smell bread?"};

	

	// creates a new player and a board
	Player* player = new Player();
	Board* gameBoard = new Board();

	// print the introductory text
	printFile("introduction.txt");
	system("pause");

	// gets players name, difficulty level and elements they want to use in the game
	getPlayerDetails(player,gameBoard,level,elements);

	// initializes the board and guesses vector in the Board class/
	gameBoard->initializeBoard();
	gameBoard->initializeGuesses();

	// prints some text to the player before the game starts
	printFile("beforeGame.txt");
	system("pause");

	// generates the secret code.
	generateSecretCode(secretCode, gameBoard,elements);

	while (true){	

		// tells the user what round it is
		cout << "ROUND: " << gameBoard->getRounds() << endl;
		
		// If player runs out of turns, then its game over
		if (gameBoard->getRounds() == gameBoard->getRows()) {
			player->setPlayerGamesPlayed(player->getPlayerGamesPlayed() + 1);
			cout << "Master Kaiju: The secret code is " + secretCode << endl;
			gameOver(player);
			// player can choose to play again
			if (restartGame(gameBoard, player, secretCode, elements, hasUsedHint, level)) {
				continue;
			}
			else {
				// If player does not want to continue anymore
				break;
			}
		}

		string option;

		// prints the menu and asks user to choose an option from the menu
		printFile("menu.txt");
		cout << "Choose one option, " + level << endl;
		cin >> option;

		// option 1 means the user wants to make a guess
		if (option == "1") {

			// displayes the symbols of the code to the user
			cout << "The symbols of the code are: " << elements << endl;
			makeGuess(gameBoard, secretCode);
			//cout << gameBoard->getGuess(rounds) << endl;
			
			// checks if code is broke or not.
			if (isCodeBroken(secretCode, gameBoard->getGuess(gameBoard->getRounds()))) {
				// wins and number of games played are updated
				player->setPlayerGamesPlayed(player->getPlayerGamesPlayed() + 1);
				player->setPlayerWins(player->getPlayerWins() + 1);

				// updates the number of rounds
				gameBoard->updateRounds();
				printFile("endMessage.txt");

				// displayes player score
				displayScore(player, gameBoard);

				// if player chooses to play again, game resets
				if (restartGame(gameBoard, player, secretCode, elements, hasUsedHint, level)) {
					continue;
				}
				else {
					break;
				}
			}

			// picks a random string from the list to "talk" to the player
				int randomNum = rand() % talkingList.size();
				cout << talkingList[randomNum] << endl;
				gameBoard->updateRounds();
		}

		// option number two means that the player wants to display the rules
		else if (option == "2") {

			// prints the rules
			printFile("rules.txt");
		}

		// option number three means that the player wants to get a hint
		else if (option == "3") {
			if (hasUsedHint == false) {

				// displays a hint if it hasn't been already used up
				getHint(secretCode, hasUsedHint);
			}
			else {

				// prints a message if player has'nt used up their hint
				cout << "Zhu: Pssst, You have already used up your hint !" << endl;
			}
		}

		// option number 4 means that the player wants to resign the mission.
		else if (option == "4") {
			if (resignMission(secretCode, player)) {
				gameOver(player);
				if (restartGame(gameBoard, player, secretCode, elements, hasUsedHint, level)) {
					continue;
				}
				else {
					cout << "THANK YOU FOR PLAYING";
;					break;
				}
			}
		}

		// option number 5 means that the player wants to quit the game.
		else if (option == "5") {
			if (quitMission(player)) {
				gameOver(player);
				cout << "--------------------" << endl;
				cout << "YOUR SCORE: " << (*player).getScore() << endl;
				cout << "--------------------" << endl;
				cout << "NUMBER OF GAMES WON: " << (*player).getPlayerWins() << endl;
				cout << "NUMBER OF GAMES PLAYED: " << (*player).getPlayerGamesPlayed() << endl;
				break;
			}
		}

		// asks player to key in correct input
		else {
			cout << "Please only select the numbers 1,2,3,4 or 5!" << endl;
		}
	}
}

// This function displays the score of the user after he/she has won.
void displayScore(Player* player,Board* board) {
	int rowsLeftScore = 0; 
	int winningScore = 0;

	// scores are calculated depending on the level of difficulty
	if (player->getDifficulty() == "1") {
		rowsLeftScore = (board->getRows() - board->getRounds()) * 2;
		winningScore = 10;
	}
	else if (player->getDifficulty() == "2") {
		rowsLeftScore = (board->getRows() - board->getRounds()) * 4;
		winningScore = 15;
	}
	else if (player->getDifficulty() == "3") {
		rowsLeftScore = (board->getRows() - board->getRounds()) * 6;
		winningScore = 20;
	}

	// totals the score
	(*player).setScore(player->getScore()+rowsLeftScore + winningScore);

	// prints the end message and score
	cout << "" <<endl;
	cout << "------------------------" << endl;
	cout << "YOUR SCORE: " << (*player).getScore() << endl;
	cout << "------------------------" << endl;
	cout << "NUMBER OF GAMES WON: " << (*player).getPlayerWins() << endl;
	cout << "NUMBER OF GAMES PLAYED: " << (*player).getPlayerGamesPlayed() << endl;
	cout << "------------------------" << endl;
}

// This function is used when the player wants to resign from the mission.
bool resignMission(string secretCode,Player* player) {
	string answer;
	bool flag = false;

	// This loop is to validate user input and ask the player if he really wants to quit or not
	while (flag != true) {
		cout << "Are you sure you want to resign this game?" << endl;
		cout << "Answer 'y' if you want to resign this game and 'n' if you don't" << endl;
		cin >> answer;

		// if player wants to quit, secret code is displayed and the game is over
		if (answer == "y") {
			cout << "Master Kaiju: The secret code is " + secretCode << endl;
			player->setPlayerGamesPlayed(player->getPlayerGamesPlayed() + 1);
			flag = true;
			return true;
		}

		// if the player decides to continue playing, the game continues
		else if (answer == "n") {
			flag = true;
			return false;
		}

		// asks player to select y or n only
		else {
			cout << "Please select either 'y' or 'n' only!" << endl;
		}
	}
	
}

// This function is used when the player wants to quit the mission
bool quitMission(Player* player) {
	string answer;
	bool flag = false;

	// This loop is to validate user input and ask the player if he really wants to resign or not
	while (flag != true) {
		cout << "Are you sure you want to quit the game?" << endl;
		cout << "Answer 'y' if you want to quit the game and 'n' if you don't" << endl;
		cin >> answer;

		// if player wants to resign, the game is over, secret code is not displayed
		if (answer == "y") {
			flag = true;
			return true;
		}
		// if player wants to continue playing, the game continued
		else if (answer == "n") {
			flag = true;
			return false;
		}
		else {
			// asks player to select y or n only
			cout << "Please select either 'y' or 'n' only!" << endl;

		}
	}
}

// This function allows the player to restart the game
bool restartGame(Board* board, Player* player,string &secretCode, string &elements,bool &hasUsedHint, string &level) {
	string answer = "";
	bool flag = false;

	// this while loop is to validate players input
	while (flag != true) {
		cout << "Do you want to play again?" << endl;
		cout << "Answer 'y' if you want to play again and 'n' to quit the game" << endl;
		cin >> answer;

		// If player wants to play again, everything is reset
		if (answer == "y") {
			board->resetBoard();
			secretCode = "";
			elements = "";
			level = "";
			hasUsedHint = false;

			// asks player to choose elements and difficulty again
			getElementsAndDifficulty(player, board, level, elements);
			board->initializeBoard();
			board->initializeGuesses();

			// generates another secret code
			generateSecretCode(secretCode, board, elements);
			flag = true;
			return true;

		}
		// If player does not want to play again, thank you message and score is printed
		else if (answer == "n") {
			cout << "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" << endl;
			cout << "THANK YOU FOR PLAYING!" << endl;
			cout << "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" << endl;
			cout << "------------------------" << endl;
			cout << "NUMBER OF GAMES WON: " << (*player).getPlayerWins() << endl;
			cout << "NUMBER OF GAMES PLAYED: " << (*player).getPlayerGamesPlayed() << endl;
			cout << "------------------------" << endl;
			flag = true;
			return false;
		}
		else {
			// asks player to select y or n only
			cout << "Please select either 'y' or 'n' only!" << endl;
		}
	}
}


// This function is for when the player wants to get a hint from Zhu
void getHint(string secretCode, bool &hasUsedHint) {

	// prints the hint file
	printFile("hint.txt");
	string hint = "";

	// takes a random element and tells the player what it is and its position
	srand(unsigned(time(NULL)));
	int randomNum = rand() % secretCode.size();
	hint = secretCode[randomNum];
	randomNum += 1;
	cout << "The element is: " + hint + " at position " << randomNum << endl;
	cout << "POOF" << endl;
	cout << "Master Zhu has now dissapeared and so has your hint!" << endl;

	// To make sure the player has only one hint, this variable is set to True.
	hasUsedHint = true;
}

// This function is to check whether a letter is in a string or not
bool isLetterInString(char letter, string &aString) {
	for (int i = 0; i < aString.size(); i++) {
		if (letter == aString[i]){
			// replaces the letter in the string with a symbol to signify that it has been evaluated 
			aString.replace(i, 1, ":");
			// returns true if the letter is in the string
			return true;
		}
	}
	return false;
}

// This function is to get the symbol representation of how well their guess matches the actual secret code
string getSymbolRep(string guess,string secretCode) {
	string returnString = "";
	string symbol = ":";

	// checks for same letter, same position (represented by 'o')
	int actualSize = secretCode.size();
	for (int i = 0; i < actualSize; i++) {
		if (secretCode[i] == guess[i]) {
			returnString += "o";

			// If there is a match, replace the code and guess with symbols, so that they're not checked twice
			secretCode.replace(i,1,":");
			guess.replace(i, 1, "'");
		}
	}

	// checks for same letter but not the right position
	actualSize = secretCode.size();
	for (int i = 0; i < actualSize; i++) {
		if (isLetterInString(guess[i], secretCode)) {
			returnString += "+";
			guess.replace(i, 1, ";");

		}
	}

	// for all the wrong characters which dont match
	actualSize = secretCode.size();
	for (int i = 0; i < actualSize; i++) {
		if (secretCode[i] != ':'){
			returnString += "_";
		}
	}
	return returnString;

}

// This function allows the player to make a guess
void makeGuess(Board* board,string secretCode) {
	string guess;
	cout << "Enter your guess: " << endl;
	cin >> guess;

	// Error handling for players guess
	while (guess.size() != board->getColumns()) {
		cout << "Enter a word of length " << board->getColumns() << endl;
		cout << "Enter your guess: " << endl;
		cin >> guess;
	}

	// gets the symbol representation of how the players guess matches the secret code
	string symbolString = getSymbolRep(guess, secretCode);

	// updates the board
	(*board).updateBoard((*board).getRounds(), guess);
	// updates the previous moves
	(*board).updateGuesses((*board).getRounds(), symbolString);

	// prints the board
	cout << (*board).printBoard();

	
}

// This function is used when the game is over, it displays the end game text and thanks the player for playing
void gameOver(Player* player) {
	cout << "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"<< endl;
	cout << "THANK YOU FOR PLAYING!" << endl;
	cout << "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" << endl;
	printFile("gameOver.txt");
	cout << "Nice try, " + player->getName() << endl;
	cout << "It seems like Master Kaiju has won this round." << endl;
	cout << "But fear not! There's always a next time!" << endl;

}

// generate a secret code according to the number of columns (length of code)
void generateSecretCode(string &code,Board* board,string &elements) {
	srand(unsigned(time(NULL)));
	vector<string> codeList;
	vector<vector<string>> wordsList;

	// produces random codes for different types of elements that are selected by the user
	if (elements == "1" || elements == "2" || elements == "3") {
		if (elements == "1") {
			codeList = { "G","B","R","Y","P","W" };
			elements = "{ G,B,R,Y,P,W }";
		}
		else if (elements == "2") {
			codeList = { "@","#","$","&","!",">","?" };
			elements = "{ @,#,$,&,!,>,? }";
		}
		else if (elements == "3") {
			codeList = { "1","2","3","4","5","6" };
			elements = "{1,2,3,4,5,6,7}";
		}
		// generates the random code
		for (int i = 0; i < board->getColumns(); i++) {
			int randomNum = rand() % board->getColumns();
			code += codeList[randomNum];
		}
	}
	// picks random words from the list of vectors to be used as the code, depending on column size
	else {
		if (elements == "4" && board->getColumns() == 4) {
			wordsList = { {"s","t","a","r"},{"m","o","o","n"},{"r","o","c","k"},{"s","h","i","p"} };
		}
		else if (elements == "4" && board->getColumns() == 5) {
			wordsList = { {"s","p","a","c","e"},{"a","l","i","e","n"},{"e","a","r","t","h"},{"m","i","l","k","y"} };
		}
		else if (elements == "4" && board->getColumns() == 6) {
			wordsList = { {"c","r","a","t","e","r"},{"p","l","a","n","e","t"},{"s","a","t","u","r","n"},{"u","r","a","n","u","s"} };

		}
		// picks a random word from the word lists and sets it as the code
		int randomNum = rand() % 4;
		vector<string> word = wordsList[randomNum];
		for (int i = 0; i < board->getColumns(); i++) {
			code += word[i];
		}
		elements = "{lowercase letters [a-z]}";
	}
}

// returns True if the code matches the user input
bool isCodeBroken(string code,string userInput) {
	return code == userInput;
}

// gets the players detais such as their name, level of difficulty and elements they want to use
void getPlayerDetails(Player* player, Board* board, string& level, string& elements) {
	string name;
	cout << "--------------------------------------------------------" << endl;
	cout << "Greetings fellow space ranger. What is your name?" << endl;
	cout << "--------------------------------------------------------" << endl;
	cin >> name;

	// sets the players name
	player->setName(name);
	cout << "Hello " + name + ". Thats an amazing name!" << endl;
	cout << "" << endl;
	getElementsAndDifficulty(player, board, level, elements);
}

// This function gets the elements the player wants to use and the level of difficulty of the game
void getElementsAndDifficulty(Player* player, Board* board, string& level, string& elements) {
	cout << "Difficulty levels:" << endl;
	cout << "--------------------------------------------------------" << endl;
	cout << "[1] Space Cadet (4 things to guess, 10 chances)\n";
	cout << "[2] Cosmic Commander (5 things to guess, 12 chances)\n";
	cout << "[3] Galactic Hero (6 things to guess, 14 chances)\n";
	cout << "--------------------------------------------------------" << endl;

	string difficulty;
	bool flag = false;
	while (flag == false) {
		cout << "What would be your preffered difficulty level?" << endl;
		cin >> difficulty;
		// sets the players difficulty
		player->setDifficulty(difficulty);
		if (player->getDifficulty() == "1") {
			cout << "Ah, good choice young Space Cadet!\n";
			level = "Space Cadet";
			// sets the rows and columns in the board class
			(*board).setRows(10);
			(*board).setCol(4);
			flag = true;
		}
		else if (player->getDifficulty() == "2") {
			cout << "Up for some friendly challenge are we, Cosmic Commander!\n";
			level = "Cosmic Commander";
			// sets the rows and columns in the board class
			(*board).setRows(12);
			(*board).setCol(5);
			flag = true;
		}
		else if (player->getDifficulty() == "3") {
			cout << "My my, get ready for some mind-boggling code breaking, Galactic Hero!\n";
			level = "Galactic Hero";
			// sets the rows and columns in the board class
			(*board).setRows(14);
			(*board).setCol(6);
			flag = true;
		}
		else {
			cout << "Please enter the option 1,2 or 3 only !\n";
		}

	}

	// Gets the elements that the player wants to use throughut the game
	cout << "Types of Elements:" << endl;
	cout << "--------------------------------------------------------" << endl;
	cout << "[1] Alphabets: [G,B,R,O,Y,P,W]" << endl;
	cout << "[2] Symbols: [@,#,$,&,!,>,?]" << endl;
	cout << "[3] Numbers: [1,2,3,4,5,6,7]" << endl;
	cout << "[4] Words: lowercase letters [a-z]" << endl;
	cout << "--------------------------------------------------------" << endl;

	// validates user input for choosing elements
	bool flag2 = false;
	while (flag2 == false) {
		cout << "What would be the elements you want to use?" << endl;
		cin >> elements;
		if (elements == "1") {
			elements = "1";
			flag2 = true;
		}
		else if (elements == "2") {
			elements = "2";
			flag2 = true;
		}
		else if (elements == "3") {
			elements = "3";
			flag2 = true;
		}
		else if (elements == "4") {
			elements = "4";
			flag2 = true;
		}
		else {
			cout << "Please enter the option 1,2 or 3 only !\n";
		}

	}

}

// This function prints a file. It is reusable function and is used many times in this assginment
void printFile(string filename) {
	// opens the file
	ifstream fileToRead;
	fileToRead.open(filename);

	// checks if the file can be opened and prints error message if it cant.
	if (!fileToRead) {
		cout << "The file can't be opened.\n";
	}

	// reads the file and outputs the lines from the file.
	while (getline(fileToRead, filename)) {
		cout << filename << "\n";
	}
	fileToRead.close();

}

