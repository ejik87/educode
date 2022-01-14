#include <iostream>
#include <math.h>
#include <float.h>
#include <iomanip> // манипуляторы выравнивания текста

//методичка страница 91

using namespace std;

void cicle_func(float a, float b, float h, int key)
{
    switch(key)
    {
    case 1: {
        cout << " " << endl;
        cout << "Cicle FOR" << endl;
        cout << " " << endl;
        cout << "  X   |     Y  " << endl;
        cout << "_______________"<< endl;
        float x, y;
        for (x = a; x <= b; x += h)
        {
            y = pow(x, 3.)*cos(x + 3.);
            cout << setw(4) << x << "  " << setw(7) << setprecision(4) << y << endl;
        }
    break;};

    case 2: {
        cout << " " << endl;
        cout << "Cicle While" << endl;
        cout << " " << endl;
        cout << "  X   |     Y  " << endl;
        cout << "_______________"<< endl;
        float x, y;
        x = a;
        while (x <= b)
        {
            y = pow(x, 3.)*cos(x + 3.);
            cout << setw(4) << x << "  " << setw(7) << setprecision(4) << y << endl;
            x += h;
        }
    break;};

    case 3:{
        cout << " " << endl;
        cout << "Cicle Do While" << endl;
        cout << " " << endl;
        cout << "  X   |     Y  " << endl;
        cout << "_______________"<< endl;
        float x, y;
        x = a;
        do
        {
            y = pow(x, 3.)*cos(x + 3.);
            cout << setw(4) << x << "  " << setw(7) << setprecision(4) << y << endl;
            x += h;
        } while (x <= b);
    break;};

    default:{cout << "Enter variant is not mach"; break;};
    }
};

int main()
{
	float a, b, h;
    int key;
    cout << "Enter a, b and step for funkshin: " << endl;
    cin >> a >> b >> h;
    cout << "Enter number variant cicle or Enter: " << endl;
    cin >> key;
    cicle_func(a, b, h, key);

//system("pause");
return 0;
};
