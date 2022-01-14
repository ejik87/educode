#include <iostream>
#include <math.h>
#include <float.h>
#include <iomanip>

using namespace std;

//методичка страница 91

int main()
{

    int A[100];
    int n;
    cout << "Enter n:";
    cin >>n;
    for (int i = 0; i<n; i++)
    {
        cout << "Enter A[" << i << "] =";
        cin >> A[i];
    };
system("pause");
return 0;
}