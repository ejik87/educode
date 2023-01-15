#include <iostream>
// #include <float.h>
#include <cmath>
#include <iomanip> // манипуляторы выравнивания текста
using namespace std;
//  Вариант 1

//  a / base- это член ряда / начальное значение .
//  n - это порядновый номер члена ряда
//  eps - это точность для вычисления ряда
//  S - сумма ряда
//  x - это аргумент

float Fx(float base, float x)
{
    float eps=0.001;
    int n=0;
    float a=1;
    float S=a;
    while (fabs(a)>eps)
    {
        a=a*(x*log(base)/(n+1));
        // cout << "a" << n << "= " << a << endl;  // Debug
        S=S+a;
        n++;
    };
return S;
};

int main()
{
    float base, x, h, step, lm;
    cout << "Calulate the sum of a series whith f ginen precision \n";
    cout << "Enter a, x, step and limit for function: " << endl;
    cin >> base >> x >> step >> lm;
    if (base>0)
    {
    cout << " " << endl;
    cout << " X  |  Y  |  clib math" << endl;
    while(x <= lm)
    {
    cout << x << "  |  " << Fx(base,x) << " | " << exp(x*log(base)) << endl;
    x=x+step;
    };
    }
    else
    {
    cout << "Enter 'a' must be > 0" << endl;
    }

return 0;
}
