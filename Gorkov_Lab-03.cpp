#include <iostream> // подключение: библиотека для консольного ввода/вывода
#include <cmath>
#include <iomanip> // манипуляторы выравнивания текста
using namespace std;
int main()
{
    float a, b, h;
    cout << "Enter a, b and step for funkshin: " << endl;
    cin >> a >> b >> h;
    float x, y;
    cout << " " << endl;
    cout << "Cicle FOR" << endl;
    cout << " " << endl;
    cout << "  X   |     Y  " << endl;
    cout << "_______________"<< endl;
    for (x = a; x <= b; x += h)
    {
        y = pow(x, 3.)*cos(x + 3.);
        cout << setw(4) << x << "  " << setw(7) << setprecision(4) << y << endl;
    }
    cout << " " << endl;
    cout << "Cicle While" << endl;
    cout << " " << endl;
    cout << "  X   |     Y  " << endl;
    cout << "_______________"<< endl;
    x = a;
    while (x <= b)
    {
        y = pow(x, 3.)*cos(x + 3.);
        cout << setw(4) << x << "  " << setw(7) << setprecision(4) << y << endl;
        x += h;
    }
    cout << " " << endl;
    cout << "Cicle Do While" << endl;
    cout << " " << endl;
    cout << "  X   |     Y  " << endl;
    cout << "_______________"<< endl;
    x = a;
    do
    {
        y = pow(x, 3.)*cos(x + 3.);
        cout << setw(4) << x << "  " << setw(7) << setprecision(4) << y << endl;
        x += h;
    } while (x <= b);
    return 0;
}