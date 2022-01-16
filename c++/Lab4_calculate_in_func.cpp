#include <iostream>
#include <math.h>
#include <float.h>

using namespace std;

float Y(float a, float b, float c, float x)
{
	return (pow(a, 3) * x - cos(x)) / (x + b * c);
};


float Z(float a, float b, float c, float x)
{
	return -pow(10., -2) * ((b*c)/x) * pow(cos(x), 2) * sqrt(pow(a, 3) * x);
};

int main()
{
	float a,b,c,x;
	cout << "Enter a b c x:";
	cin >> a >> b >> c >> x;
	if (c != 0 && a > 0 && x > 0 && b != 0)
	{
	float y = Y(a,b,c,x);
	float z = Z(a,b,c,x);
	float S = y + z;

	cout << "Y: " << y << endl;
	cout << "Z: " << z << endl;
	cout << "S: " << S << endl;
	}
	else
	{
		cout << "Arguments non equel null";
	}

//system("pause");
return 0;
};
