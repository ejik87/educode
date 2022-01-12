#include <iostream> // подключение: библиотека для консольного ввода/вывода
#include <cmath>
using namespace std;
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