#include <iostream> // подключение: библиотека для консольного ввода/вывода
#include <cmath>
using namespace std;    //обозначение пространства имён. нужно чтобы работало, иначе каждый раз нужно задавать std
int main()
{
    float a, b, c, x, y, z, S;
    cout << "Enter a, b, c ,x: "; //сообщение для ввода
    cin >> a >> b >> c >> x;
    if (a != 0)
    {
    y = 2.5*((a*b*(x*x))/2.) + log((x + a)*c);
    z = pow(10., -1.)*((sqrt(x - a))/(a*(x*x))) - cos((x + a)*c);
    S = y +z;
    cout << "S = " << S << endl;
    cout << "z= " << z << endl;
    }   else {
        cout << "Result not calculation" << endl; // вывод сообщения при не подходящем значении
    };
    return 0;
}