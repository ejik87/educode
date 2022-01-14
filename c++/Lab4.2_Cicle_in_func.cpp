#include <iostream>
#include <math.h>
#include <float.h>
#include <iomanip> // манипуляторы выравнивания текста

//методичка страница 91

using namespace std;

void print_head(string head)
{
    cout.width(15);  // Устанавливаем ширину вывода жестко.
    cout << '\n' << head << '\n' << endl;  // для переноса строк используем спец символы.
    cout << setiosflags(ios::left) << setw(5)  << "X" << resetiosflags(ios::left)  << setw(10) << "Y" << endl;
    //cout << "  X   |     Y  " << endl;
    //cout.fill('.');  // Заполняет пробелы символами из скобок.
    cout << "_______________" << "\n" << endl;
};

void print_table(int x, float y)
{   // Немного форматирования по левому краю, затем сброс форматирования -> прижимает к правому краю и округляем до 5 символов в общем.
    cout << setiosflags(ios::left) << setw(5)  << x << resetiosflags(ios::left)  << setprecision(5) << setw(10) << y << endl;
};

void cicle_func(float a, float b, float h, int key)
{
    switch(key)
    {
    case 1: {
        string head = "Cicle For";
        print_head(head);
        float x, y;
        for (x = a; x <= b; x += h)
        {
            y = pow(x, 3.)*cos(x + 3.);
            //cout << setw(4) << x << "  " << setw(7) << setprecision(4) << y << endl;  // старый варик
            print_table(x,y);

        }
    break;};

    case 2: {
        string head = "Cicle While";
        print_head(head);
        float x, y;
        x = a;
        while (x <= b)
        {
            y = pow(x, 3.)*cos(x + 3.);
            print_table(x,y);
            x += h;
        }
    break;};

    case 3:{
        string head = "Cicle Do While";
        print_head(head);
        float x, y;
        x = a;
        do
        {
            y = pow(x, 3.)*cos(x + 3.);
            print_table(x,y);
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
