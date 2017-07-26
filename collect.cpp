#include <bits/stdc++.h>

#define pii pair <int, int> 

using namespace std;

int main()
{
	int n, m;
	cin >> n >> m;

	char A[n][m];

	for(int i = 0; i < n; i++)
		cin >> A[i];

	/* Find next move and output 
	 * Valid moves:
	 * "left"
	 * "rightt"
	 * "down"
	 * "up"
	 */

	char S[n + 5][m + 5];
	memset(S, 'W', sizeof(S));

	for(int i = 0; i < n; i++)
		for(int j = 0; j < m; j++)
			S[i + 1][j + 1] = A[i][j];

	pii cur;
	for(int i = 1; i <= n; i++)
		for(int j = 1; j <= m; j++)
			if(S[i][j] == 'P')
			{
				S[i][j] = 'V';
				cur = {i, j};
			}

	pii des;
	for(int i = 1; i <= n; i++)
		for(int j = 1; j <= m; j++)
			if(S[i][j] == 'o')
			{
				des = {i, j};
				break;
			}

	queue < pair < pii, string > > Q;

	Q.push({cur, ""});

	while(not Q.empty())
	{
		auto p = Q.front();
		Q.pop();

		int x, y;
		tie(x, y) = p.first;

		string P = p.second;

		if(p.first == des)
		{
			switch(P[0])
			{
				case 'U': cout << "up" << endl; break;
				case 'L': cout << "left" << endl; break;
				case 'D': cout << "down" << endl; break;
				case 'R': cout << "right" << endl; break;
			}

			return 0;
		}

		if(S[x + 1][y + 0] != 'W' and S[x + 1][y + 0] != 'V')
		{
			S[x + 1][y + 0] = 'V';
			Q.push({{x + 1, y + 0}, P + "D"});
		}

		if(S[x - 1][y - 0] != 'W' and S[x - 1][y - 0] != 'V')
		{
			S[x - 1][y - 0] = 'V';
			Q.push({{x - 1, y - 0}, P + "U"});
		}
		
		if(S[x + 0][y + 1] != 'W' and S[x + 0][y + 1] != 'V')
		{
			S[x + 0][y + 1] = 'V';
			Q.push({{x + 0, y + 1}, P + "R"});
		}
		
		if(S[x - 0][y - 1] != 'W' and S[x - 0][y - 1] != 'V')
		{
			S[x - 0][y - 1] = 'V';
			Q.push({{x - 0, y - 1}, P + "L"});
		}
	}

	return (0-0);	
}