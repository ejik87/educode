#include <iostream>
// #include <float.h>
#include <cmath>
#include <iomanip> // манипуляторы выравнивания текста
using namespace std;

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
    cout << "Enter a, x, step and limit for function: " << endl;
    cin >> base >> x >> step >> lm;
    if (base>0)
    {
    cout << " " << endl;
    cout << " X  |  Y  |  Math" << endl;
    while(x <= lm)
    {
    cout << x << "  |  " << Fx(base,x) << " | " << exp(x*log(base)) << endl;
    x=x+step;
    };
    }
    else
    {
    cout << "a need > 0" << endl;
    }

return 0;
}
