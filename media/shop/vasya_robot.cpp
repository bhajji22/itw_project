#include<bits/stdc++.h>
using namespace std;
int main()
{
	int n,l,r,ql,qr;
	cin>>n>>l>>r>>ql>>qr;
	int ar[n];
	for(int i=0;i<n;i++)
		cin>>ar[i];
	int prel[n+1];
	int prer[n+1];
	int s=0;prel[0]=0;prer[n]=0;
	for(int i=1;i<=n;i++)
	{
		s+=ar[i-1];
		prel[i]=s;
	}
	s=0;
	for(int i=n-1;i>=0;i--)
	{
		s+=ar[i];
		prer[i]=s;
	}
	int max = INT_MAX;
	for(int i=0;i<=n;i++)
	{
		int v=0;
		int k = n-2*i-1;
		int sum = l*prel[i]+ r*prer[i];
		if(abs(i-(n-i))<=1)
		{}
		else
		{
			v = (k>0)?k*qr:-(k+2)*ql;
		}
		if(max>v+sum)
			max = v+sum;
		//cout<<sum<<" "<<v<<endl;
	}
	cout<<max;
}