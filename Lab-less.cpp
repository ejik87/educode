#include <iostream> // подключение: библиотека для консольного ввода/вывода
#include <cmath>
using namespace std;    //обозначение пространства имён. нужно чтобы работало, иначе каждый раз нужно задавать std
int main()
{
    float z1, z2, x;
    cout << "Enter x: "; //сообщение для ввода Х
    cin >> x;
    z1 = (x*x + 2.0*x - 3.0 + (x+1.0)*sqrt(x*x-9.0))/(x*x - 2.0*x - 3.0 + (x+1.0)*sqrt(x*x-9.0));
    z2 = sqrt((x+3.0)/(x-3.0));
    cout << "z1 = " << z1 << endl;
    cout << "z2 = " << z2 << endl;
    return 0;
}