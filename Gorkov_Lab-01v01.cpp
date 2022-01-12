#include <iostream> // подключение: библиотека для консольного ввода/вывода
#include <cmath>
using namespace std;    //обозначение пространства имён. нужно чтобы работало, иначе каждый раз нужно задавать std
int main()
{
    float z1, z2, x, a;
    cout << "Enter x, a: "; //сообщение для ввода Х
    cin >> x >> a;
    z1 = (2.*(sin(3.*M_PI - 2.*a)*sin(3.*M_PI - 2.*a))*(cos(5.*M_PI + 2.*a)*cos(5.*M_PI + 2.*a)));
    z2 = 1./4. - 1./4.*(sin((5.0/2.)*M_PI - 8.*a));
    cout << "z1 = " << z1 << endl;
    cout << "z2 = " << z2 << endl;
    return 0;
}