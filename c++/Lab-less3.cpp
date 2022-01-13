#include <iostream> // подключение: библиотека для консольного ввода/вывода
#include <cmath>
using namespace std;    //обозначение пространства имён. нужно чтобы работало, иначе каждый раз нужно задавать std
int main()
{
    float a, b, c, x, y, z, S;
    cout << "Enter a, b, c ,x: "; //сообщение для ввода
    cin >> a >> b >> c >> x;

if (b != 0 && c != 0 && cos(x/b) != 0 && (a/c) != 0)
{
    y = tan(x/b) * log(a/c);
    z = cos((a*x)/(b*c));
    S = y +z;
    cout << "S = " << S << endl;
}   else
{
    cout << "Function not calculated!" << endl;
};
return 0;
}