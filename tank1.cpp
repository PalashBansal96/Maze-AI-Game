#include <iostream>
#include <map>

using namespace std;

string moves[] = {"up", "down", "left", "right", "upleft", "upright", "downleft", "downright"};
int valid_pos[] = {0, 1, 2, 3, 4, 5, 6, 7};
const int MAX_SIZE = 100;
const int inf  = 1e6;

char grid[MAX_SIZE][MAX_SIZE];

int hd(int x1, int y1, int x2, int y2)
{
	return abs(x1 - x2) + abs(y2 - y1);
}

int main()
{
	int n, m;
	cin >> n >> m;
	char curr;
	cin >> curr;
	char myChar = '1';
	char myNinja = 'A';
	int myPosi = -1, myPosj = -1;
	int myNinjaI, myNinjaJ;
	string input;
	for(int i = 1; i <= n; i++)
	{
		cin >> input;
		for(int j = 1; j <= m; j++)
		{
			grid[i][j] = input[j - 1];
			if(grid[i][j] == myChar)
			{
				myPosi = i;
				myPosj = j;
			}
			else if(grid[i][j] == myNinja) {
				myNinjaI = i; myNinjaJ = j;
			}
		}
	}
	if(myChar != curr){
		return 0;
	}
	for(int i = 0; i <= m + 1; i++) {
		grid[0][i] = 'W';
		grid[n + 1][i] = 'W';
	}
	for(int i = 0; i <= n + 1; i++) {
		grid[i][0] = 'W';
		grid[i][m + 1] = 'W';
	}
	int poss_moves[8];
	if(grid[myPosi][myPosj - 1] == 'W') {
		poss_moves[0] = inf;
	}
	else {
		poss_moves[0] = hd(myPosi, myPosj - 1, myNinjaI, myNinjaJ);
	}
	if(grid[myPosi][myPosj + 1] == 'W') {
		poss_moves[1] = inf;
	}
	else {
		poss_moves[1] = hd(myPosi, myPosj + 1, myNinjaI, myNinjaJ);
	}
	if(grid[myPosi - 1][myPosj] == 'W') {
		poss_moves[2] = inf;
	}
	else {
		poss_moves[2] = hd(myPosi - 1, myPosj, myNinjaI, myNinjaJ);
	}
	if(grid[myPosi + 1][myPosj] == 'W') {
		poss_moves[3] = inf;
	}
	else {
		poss_moves[3] = hd(myPosi + 1, myPosj, myNinjaI, myNinjaJ);
	}
	if(grid[myPosi - 1][myPosj - 1] == 'W') {
		poss_moves[4] = inf;
	}
	else {
		poss_moves[4] = hd(myPosi - 1, myPosj - 1, myNinjaI, myNinjaJ);
	}
	if(grid[myPosi + 1][myPosj - 1] == 'W') {
		poss_moves[5] = inf;
	}
	else {
		poss_moves[5] = hd(myPosi + 1, myPosj - 1, myNinjaI, myNinjaJ);
	}
	if(grid[myPosi - 1][myPosj + 1] == 'W') {
		poss_moves[6] = inf;
	}
	else {
		poss_moves[6] = hd(myPosi - 1, myPosj + 1, myNinjaI, myNinjaJ);
	}
	if(grid[myPosi + 1][myPosj + 1] == 'W') {
		poss_moves[7] = inf;
	}
	else {
		poss_moves[7] = hd(myPosi + 1, myPosj + 1, myNinjaI, myNinjaJ);
	}
	int minDev = inf;
	int newPos;
	for(int i = 0; i < 8; i++)
	{
		if(poss_moves[i] < minDev) 
		{
			minDev = poss_moves[i];
			newPos = i;
		}
	}
	cout << moves[newPos] << endl;
	return 0;
}