#include <iostream>
#include <stdlib.h> 
#include <time.h>
using namespace std;

int main(){
	char a[4][4];
	srand(time(0));
	for(int i=0; i<3; i++){
		for(int j=0; j<3; j++){
			cin>>a[i][j];
		}
	}
	int moves[9] = {1,2,3,4,5,6,7,8,9}, lenMoves = 9;
	cout<<moves[rand()%lenMoves]<<endl;
	return 0;
}