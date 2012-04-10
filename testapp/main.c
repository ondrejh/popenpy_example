#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <windows.h>

#define printf(...) printf(__VA_ARGS__); fflush(stdout)

int main()
{
    printf("Hello world!\n");
    //fflush(stdout);

    int cnt=1;

    //sleep(1);
    Sleep(1000);
    printf("%d little indian\n",cnt++);
    //fflush(stdout);

    while(1)
    {
        //sleep(1);
        Sleep(1000);
        printf("%d little indians\n",cnt++);
        //fflush(stdout);
    }

    return 0;
}
