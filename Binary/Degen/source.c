#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <stdbool.h>

int count;
#define ROWS 2
#define COLS 4

int ansperm()
{
    return 9059178;
}

void shuffleMatrix(int matrix[2][4]) {
    srand(84238932); 
    for (int i = 0; i < ROWS * COLS; i++) {
        int x = rand() % ROWS;
        int y = rand() % COLS;
        int z = rand() % ROWS;
        int w = rand() % COLS;
        
        int temp = matrix[x][y];
        matrix[x][y] = matrix[z][w];
        matrix[z][w] = temp;
    }
}

void deterministicShuffle(int* array, size_t n, unsigned long seed) {
    if (n > 1) {
        srand(seed);
        size_t i;
        for (i = n - 1; i > 0; i--) {
            size_t j = rand() % (i + 1);
            int tmp = array[j];
            array[j] = array[i];
            array[i] = tmp;
        }
    }
}

long long power(int a, unsigned int b, int m)
{
    long long res = 1;
    a = a % m;
    while (b > 0)
    {
        if (b & 1)
        {
            res = (res * a) % m;
        }
        a = (a * a) % m;
        b >>= 1;
    }
    return res;
}

bool func1(long long int n)
{
    if (n <= 1)
        return false;
    if (n <= 3)
        return true;

    if (n % 2 == 0 || n % 3 == 0)
    {
        return false;
    }

    for (int i = 5; i * i <= n; i = i + 6)
    {
        if (n % i == 0 || n % (i + 2) == 0)
            return false;
    }

    int k = 1;
    while (k < 100)
    {
        if (power(2, n - 1, n) != 1)
        {
            return false;
        }
        k++;
    }

    return true;
}

void swap(int *xp, int *yp)
{
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}

void permute(int *num, int l, int r)
{
    int i;
    if (l == r)
    {
        if (count > 0)
        {
            for (i = 0; i <= r; i++)
            {
                printf("%d ", num[i]);
            }
            printf("\n");
            count--;
        }
    }
    else
    {
        for (i = l; i <= r; i++)
        {
            swap(&num[l], &num[i]);
            permute(num, l + 1, r);
            swap(&num[l], &num[i]);
        }
    }
}

int square(int num)
{
    return num * num;
}

int main(int argc, char *argv[])
{
    char c[32];

    printf("Enter a number and check your luck\n");
    fgets(c, sizeof(c), stdin);

    if (strlen(c) != 31)
    {
        printf("Process Exited - Error 1");
        return 0;
    }

    int check1 = (c[15] - '0') * 1000 + (c[1] - '0') * 100 + (c[12] - '0') * 10 + (c[5] - '0');
    puts("F Little ? Why not smallest ?");

    if (!func1(check1))
    {
        printf("Process Exited - Error 2");
        return 0;
    }

    if (strlen(c) >= 4)
    {
        count = c[3] - '0';
        count = count * count;
        puts("Remember that three is the new seven\n");
    }
    else
    {
        printf("Process Exited - Error 3");
        return 0;
    }

    int matr[] = {c[0] - '0', c[2] - '0', c[4] - '0', c[6] - '0', c[8] - '0', c[10] - '0', c[14] - '0'}; //
    permute(matr, 0, 6);
    if (ansperm() == 9059178)
        puts("Group theory is fun\n");

    int sup[] = {c[7] - '0', c[9] - '0', c[11] - '0', c[13] - '0', c[10] - '0'};
    int num = sup[0] * 1000 + sup[1] * 100 + sup[2] * 10 + sup[3];

    int nextNum = 0;
    int final;

    while (num != 0)
    {
        final = num;
        nextNum = 0;
        while (num > 0)
        {
            int digit = num % 10;
            nextNum = nextNum * 10 + square(digit);
            num /= 10;
        }
        num = nextNum;
    }

    if (final != -329017116)
    {
        printf("Process Exited - Error 4");
        return 0;
    } 

    int second[] = {c[16] - '0', c[17] - '0', c[18] - '0', c[19] - '0', c[20] - '0', c[21] - '0', c[22] - '0', c[23] - '0'}; //75237253
    int sed = 49823739;

    for(int i = 0; i < 8; i++){
        deterministicShuffle(second, 8, sed);
        if(i == 6){
            int check[] = {7, 2, 3, 2, 5, 7, 3, 5};
            for(int i = 0; i < 8; i++){
                if(check[i] != second[i]){
                     puts("Uknown Error !!!");
                     return 0;
                }
            }
        }
        sed += sed/10;
    }

    int seed = c[31]*1000 + c[30]*100 + c[29]*10 + c[28]; //3257 7523
    int cum = c[24]*1000 + c[25]*100 + c[26]*10 + c[27]; //5273

    int mn[2][4];

    for(int i = 0; i < 2; i++){
        for(int j = 0; j < 4; j++){
            mn[i][j] = seed/10;
            seed = seed/10;
        }
    }

    for(int i = 1; i < 2; i++){
        for(int j = 0; j < 4; j++){
            mn[i][j] = cum/10;
            cum = cum%10;
        }
    }

    shuffleMatrix(mn);

    int ab[2][4] = {
        {5860, 0, 5, 0},
        {0, 0, 585, 58}
    };

    for(int i = 0; i < 2; i++){
        for(int j = 0; j < 4; j++){
           if(mn[i][j] != ab[i][j]){
            puts("Process Exited - Error 5");
            return 0;
           }
        }
    }

    puts("Just remember that everything always ends with a 7, SIUUUUU!!!!");

    puts("Congrats !!!");
}
