#include <iostream>
#include <math.h>
//#include <float.h>
//#include <cstdlib.h>
using namespace std;

void max_int(int AA[], int n)
{
    int max = abs(AA[0]);
    for (int i = 1; i < n; i++)
    {
        if (max < abs(AA[i]))
        {
            max = abs(AA[i]);
        };
    };
    cout << "\nMaximum number: " << max << endl;
}

void find_count(int AA[], int n)
{
    int num;
    cout << "Enter integer num to find in massive: " << ends;
    cin >> num;
    cout << "Count mach " << num << ": " << count(AA, AA+n, num) << endl;
}

void positive_sum(int AA[], int n)
{
    int sum;
    for (int i=0; i<n; i++)
    {
        if (AA[i] % 2 == 0 && AA[i]>0)
        {
            sum += AA[i];
        }
    }
    cout << "Summ positive and chetn nums = " << sum << endl;
}

int main()
{
int n;
cout << " Enter SIZE massive: " << ends;
cin >> n;
int A[n];
for (int i = 0; i < n; i++)
{
    A[i] = (int) rand() % 101 - 50;  // числа из диапазона -50...50
};
cout << "Massive: " << ends;
for (int i = 0; i < n; i++)
{
// cout << "A[" << i << "] = " << A[i] << endl;  // вывод массива в столбец
cout << A[i] << " " << ends;  // вывод массива в ряд
};
    max_int(A, n);
    find_count(A, n);
    positive_sum(A, n);
//system (“pause”);
return 0;
}
