// Лекции осенней установочной сессии 10.2021г.

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

====================================================================================
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

==================================================================================

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

==================================================================================

int main()
{
    for (int i = 3; i < 7; i++ )  //for (int i = start; i < end; i++ ) цикл со счётчиком
    {   //тело цикла
        cout << i << endl; // 4 раза
        // break завершает цикл принудительно
    };

    // цикл с пердусловием
    k=5
    while (k > 0)  //while (условие)
    {
        cout << k << endl;
        k--; // уменьшает на еденицу
        ;// тело цикла
        // break завершает цикл принудительно
    };
    do // цикл с постусловием, работает хотябы 1 раз
    {
       cout <<k << endl;
        k--;/* code */
    } while (k > 0);


    return 0;
}

==================================================================================

int main()  // основная программа, стартовая точка
{
    // 1. Оператор вывода
    cout << "Hello, world!" << endl;    // endl перевод строки
    cout << 123 << " ";
    cout << 14*36+147-89 << endl;

    cout << "Hello, world!" << " " << 123 << " "  << 14*36+147-89 << endl;

    // 2. Переменные
    int A; // переменная А - целое число (1, 23, -4 ...)
    float B; // переменная В - вещественное число ( 1.5, 43.03, 5.0, -0.15)
    char S; // S - один любой символ ASCI S  = '*'
    char s2[10];    // S - последовательность символов (строка) S="январь"

    // 3. Оператор ввода
    //cin >> A;
    //cout << A;
    //cin >> B;
    //cout << B;

    //cin >> s2;   cout << s2;
    cin >> A >> B >> S >>s2;
    //system("pause");    //для задержки окна
    return 0;           // 0 - признак успешного завершения работы
    // 4. условный оператор (полная форма)
    if (logic.uslovie1)
    {
         // действия, если условие верно;

    }
    else if (log.uslovie2)
        {
            // если условие 2 верно
        }   else
        {
            // действия, если условие2 ложно;
        }

    // неполная форма
    if (log.uslovie)
    {

    }



};

==================================================================================
