# Slimy Guy
Let's look at a decompilation of the binary.
```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  time_t v3; // rax
  int v4; // eax
  int v5; // eax
  int v7; // [rsp+8h] [rbp-C8h] BYREF
  int v8; // [rsp+Ch] [rbp-C4h] BYREF
  int v9; // [rsp+10h] [rbp-C0h] BYREF
  __gid_t rgid; // [rsp+14h] [rbp-BCh]
  int v11; // [rsp+18h] [rbp-B8h]
  int v12; // [rsp+1Ch] [rbp-B4h]
  FILE *stream; // [rsp+20h] [rbp-B0h]
  unsigned __int64 v14; // [rsp+28h] [rbp-A8h]
  unsigned __int64 v15; // [rsp+30h] [rbp-A0h]
  unsigned __int64 v16; // [rsp+38h] [rbp-98h]
  char s[136]; // [rsp+40h] [rbp-90h] BYREF
  unsigned __int64 v18; // [rsp+C8h] [rbp-8h]

  v18 = __readfsqword(0x28u);
  setvbuf(_bss_start, 0LL, 2, 0LL);
  rgid = getegid();
  setresgid(rgid, rgid, rgid);
  v3 = time(0LL);
  srand(v3 / 60);
  signal(11, (__sighandler_t)peaceout);
  v11 = 4;
  puts("Welcome!");
  puts("0. Print flag!");
  puts("1. Hard things?");
  puts("2. Secret stuff!");
  puts("3. Do it!");
  while ( 1 )
  {
    while ( 1 )
    {
      printf("stage1> ");
      __isoc99_scanf("%d", &v7);
      v4 = v7 % 4;
      if ( v7 % 4 == 3 )
        break;
      if ( v4 <= 3 )
      {
        if ( v4 == 2 )
        {
          puts("?> ? ?");
          __isoc99_scanf("%d %d", &v8, &v9);
          v8 %= v11;
          v9 %= v11;
          v14 = (unsigned __int64)coins_0[v8];
          v15 = (unsigned __int64)coins_0[v9];
          v16 = v15 ^ v14;
          coins_0[v8] = (void *)(v15 ^ v14);
        }
        else if ( v4 <= 2 )
        {
          if ( v4 )
          {
            if ( v4 == 1 )
            {
              v5 = rand();
              puts(things[v5 % 3]);
            }
          }
          else
          {
            puts(flag);
          }
        }
      }
    }
    printf("?> ");
    __isoc99_scanf("%d", &v9);
    switch ( v9 % (v11 - 1) )
    {
      case 0:
        puts("Do you really trust me?");
        break;
      case 1:
        puts("Flags come and go my child. The learnings, however, are eternal.");
        break;
      case 2:
        puts("Follow the path which calms your mind.");
        break;
      case 3:
        puts("You seem to be a sneaky lil guy.");
        puts("I'm thinking of a number.");
        printf("If you can guess it, I'll give you the real flag> ");
        v12 = rand();
        __isoc99_scanf("%d", &v9);
        if ( v12 != v9 )
        {
          puts("Wow, nice guess! Here's the flag:");
          puts("p_ctf{");
          puts("Segmentation fault (soul dumped)");
          exit(127);
        }
        puts("Wow, nice guess! Here's the flag:");
        stream = fopen("flag.txt", "r");
        fgets(s, 128, stream);
        puts(s);
        return 0;
    }
  }
}
```
We notice that the program in seeded by the time divided by 60. Hence we know that the seed remains the same for a minute. Let's keep this in mind. Looking at the initial `stage1>` input, options 0, 1 seem to lead to just something being printed out, so we don't find much of a lead here. When we input 2, and give 2 integers `i` and `j`, it essentially seems to execute `coins_0[i] ^= coins_0[j]`.  But according to the code, `coins_0` does not seem to be used anywhere. But... when we mess with option 2, and run it with `0` and `1` for example, and then go option `3`, we get the message: `It's secret stuff for a reason. Tread carefully.`.  We also see that the `peaceout` function is registered as a signal handler for signal 11, and prints this out. Which means, an option 2 followed by option 3 has caused a signal 11, which is a `SIGSEGV`. By changing the value in the `coins_0` array, we cause a segfault, which gives us a hint that we can mess with some addresses via the `coins_0` array.

 Now let's look at option 3. Option 3 leads into another switch statement, `switch ( v9 % (v11 - 1) )`. We know `v11 = 4`, thus `v9 % (v11 - 1)` can only possibly go into cases 0, 1, 2, whereas the flag seems to printed out in case 3. Normally, this would be impossible to attain. I'm gonna run this through one more decompiler, and let's see what we get.
```c
int main()
{
    char v0;  // [bp-0xd0]
    unsigned int v1;  // [bp-0xcc], Other Possible Types: char
    char v2;  // [bp-0xc8], Other Possible Types: unsigned int
    unsigned int v3;  // [bp-0xc4]
    unsigned int v4;  // [bp-0xc0]
    unsigned long v5;  // [bp-0xb0]
    unsigned long v6;  // [bp-0xa8]
    unsigned long v7;  // [bp-0xa0]
    unsigned long v8;  // [bp-0x10]
    unsigned long long *v10;  // fs
    unsigned long long v11;  // rax
    unsigned int v12;  // eax
    unsigned long long v13;  // rax

    v8 = v10[5];
    setvbuf(__TMC_END__, NULL, 2, 0);
    v3 = getegid();
    setresgid(v3, v3, v3, v3);
    v11 = time(NULL);
    srand(((v11 * 9838263505978427529 >> 64) + v11 >> 5) - (v11 >> 63));
    signal(11, peaceout);
    v4 = 4;
    puts("Welcome!");
    puts("0. Print flag!");
    puts("1. Hard things?");
    puts("2. Secret stuff!");
    puts("3. Do it!");
    while (true)
    {
        printf("stage1> ");
        __isoc99_scanf("%d", (unsigned int)&v0);
        v12 = (*((int *)&v0) + (unsigned int)(*((int *)&v0) >> 31 >> 30) & 3) - (*((int *)&v0) >> 31 >> 30);
        if (v12 == 3)
            break;
        if (v12 <= 3)
        {
            if (v12 == 2)
            {
                puts("?> ? ?");
                __isoc99_scanf("%d %d", (unsigned int)&v1, (unsigned int)&v2);
                v1 = (v1 >> 31 CONCAT v1) /m v4 >> 32;
                v2 = (v2 >> 31 CONCAT v2) /m v4 >> 32;
                v5 = *((long long *)&(&coins.0)[8 * v1]);
                v6 = *((long long *)&(&coins.0)[8 * v2]);
                v7 = v5 ^ v6;
                *((unsigned long *)&(&coins.0)[8 * v1]) = v7;
            }
            else
            {
                if (!(v12 <= 2))
                    goto LABEL_4016e0;
                if (!v12)
                {
                    puts(flag);
                }
                else
                {
                    if (!(v12 == 1))
                        goto LABEL_4016e0;
                    (unsigned int)v13 = rand();
                    puts(*((long long *)&(&things)[16 * (v13 >> 31) + 8 * (v13 >> 31) + 8 * v13 + -8 * (v13 * 1431655766 >> 32) + -16 * (v13 * 1431655766 >> 32)]));
                }
            }
        }
LABEL_4016e0:
    }
    printf("?> ");
    __isoc99_scanf("%d", (unsigned int)&v2);
    goto *((long long *)(((*((int *)&v2) >> 31 CONCAT *((int *)&v2)) /m ((int)(stack_base)[192] - 1) >> 32) * 8 + 4210784));
}
```
We can again notice, option 2 messes with the `coins` array, and option 3 is jump into a jump table. We know that the first decompiler interpreted this as a switch statement, which is in general implemented as a jump table by compilers. We have 4 observations:
1. `coins` is an array of size 4, and we can freely xor any 2 values of this array and store it back.
2. Messing with the `coins` which seems to be not used anywhere else leads to a `SIGSEGV`.
3. Option 3 jumps into a mysterious jump table.
4. Option 3's decompiled switch statement has a unreachable case 3.

What if coins is our mysterious jump table? And what if our unreachable case is just the address being stored in our jump table at offset 3? We just need to now reach this address to get to our flag. Since we can xor 2 numbers together, we can essentially swap any 2 addresses in coins by a series of 3 xors. And then we can jump to a case after swapping! Let's try swapping `coins[0]` and then `coins[3]` and then try to jump to `coins[0]`.
```
Welcome!
0. Print flag!
1. Hard things?
2. Secret stuff!
3. Do it!
stage1> 2
?> ? ?
0 3
stage1> 2
?> ? ?
3 0
stage1> 2
?> ? ?
0 3
stage1> 3
?> 0
You seem to be a sneaky lil guy.
I'm thinking of a number.
If you can guess it, I'll give you the real flag> 
```
Well seems like our guess it true! Now we just need to guess a random number, and if it is correct, we have our flag! Since we know the seed is just `time(NULL) / 60`, we seed a program locally and get the next random number, and proceed to get our flag.


We'll have a simple program to generate the random numbers:
```c
#include  <stdlib.h>
#include  <stdio.h>
#include  <time.h>

int  main() {
	srand(time(NULL) /  60);
	int  SZ  =  3;
	for (int  i  =  0; i  <  SZ; ++i)
		printf("%d\n", rand());
}
```
We'll use this to get our flag:
```
Welcome!
0. Print flag!
1. Hard things?
2. Secret stuff!
3. Do it!
stage1> 2
?> ? ?
0 3
stage1> 2
?> ? ?
3 0
stage1> 2
?> ? ?
0 3
stage1> 3
?> 0
You seem to be a sneaky lil guy.
I'm thinking of a number.
If you can guess it, I'll give you the real flag> 579074059
Wow, nice guess! Here's the flag:
p_ctf{m3ss_w1th_g0t0s}
```