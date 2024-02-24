# Pragyan CTF 2024: Degen

`QUESTION:` Unofortunately, I've left my key in the source program and my friends have decided to play a little prank me. So I've hired you, The greatest ctf-er to help me find my key.

Looking at the question and the name of the challenge, We can identify that its gonna be a key generation challenge

We are given a single binary file, We boot it up into `GHIDRA` to see a decompiled version of the ELF. For convenience purposes, We'll be looking at the source code to truly understand the inner workings of this Binary file.

## Process 1:

<img width="695" alt="fgets" src="https://github.com/purrate/4.PCTF24/assets/132884539/af7d9627-bd8d-46c5-a946-4f8499096cd2">

Here as we can see, A string of 32 characters is declared in the local scope of the main function, And a fgets function is used to read the standard input from the user. Next, We have length checker which says that the size of the string should be equal to 31, Otherwise the process gets exited with an error 1. But how is that possible when the size of the string is supposed to be 32 and the fgets function uses the parameter of `sizeof(c)`. 

Well, The answer to that lies in how the fgets function works. 

<img width="814" alt="fgetsonline" src="https://github.com/purrate/4.PCTF24/assets/132884539/b556f366-d91c-42d6-8789-1c794b16ac0c">

As we can see, fgets function only reads `(size - 1)` no of characters leaving space for the newline character or EOF. That's why we are able to pass a string of size 32 and not get the error of `Process Error - 1`. But Now, we know that the final answer of the keygen should be 32 indiated by the declaration of the string c.

## Process 2:

<img width="720" alt="process2sc" src="https://github.com/purrate/4.PCTF24/assets/132884539/99bfb7cf-4223-41dc-886d-7598a2ad496c">

This part of the program seems to consider a 4 digit integer by using the array indices of `[15 1 12 5]`. The number that should be formed is stored inside the check1 variable and passes it through a function called func1. Let's take a closer look at the function `func1` to understand the workings of this function.

<img width="344" alt="euclid" src="https://github.com/purrate/4.PCTF24/assets/132884539/d1995ece-5e99-477a-8e52-cc209697e8d2">

As we take a closer look into it, We can see that the function `func1` checks the divisibility of all numbers of the form `6k + 1` up to the square root of n. This is an optimization to list all the odd integers but what is this function actually doing ? Finally, the function checks if n is a base for any of the first 100 powers of 2. This is done using the modular exponentiation function power(a, b, n), which calculates (a^b) % n efficiently. Then it checks if n is a base for any of these powers.

<img width="350" alt="power" src="https://github.com/purrate/4.PCTF24/assets/132884539/23cbfd4b-16cf-4278-a682-12ef483667d3">

The power function seems to be `euclids algorithm` to calculate the power of an integer which is very large in size. The `func1` function seems to be a direct derivative of `Fermats little theorem` as we can see its using `Euclids extended algorithm` to check the primality of the odd numbers. So, we know that the 4 digit number is a prime number but what about the specific number that we need ?. 

We can see that there's a cryptic that says 

**"F Little ? Why not smallest ?"**

We can assume that we are supposed to get the smallest 4 digit prime number possible in the set of integers. This should be 1009.

Now we know, `c[15] = 1, c[1] = 0, c[12] = 0, c[5] = 9`

## Process 3:

<img width="428" alt="process3sc" src="https://github.com/purrate/4.PCTF24/assets/132884539/8da08e4f-cf1b-4b3f-9d62-50cf1c09e138">

Process 3 seems rather simple with another cryptic which says 

**"Remember that three is the new seven"**

As we are using the third index to modify the value of the count variable, We can identify that the 3rd index of the string c must be 7.

We know, `c[1] = 0, c[3] = 7, c[5] = 9, c[12] = 0, c[15] = 1`

## Permutation Checker:

<img width="806" alt="anspermsc" src="https://github.com/purrate/4.PCTF24/assets/132884539/31ec3601-121b-46e5-b58d-7c68f9952f0a">

As, we can see that the, Bunch of indices of the string c is getting passed into the `permute` function as an array of integers called `matr`. But this array never gets returned or even stored. How are we supposed to figure out the integers which take a place in this index. When we look at the next line of the function call. We see another function call which gets checked with `9059178`. This function `ansperm` seems to return a static integer value that gets checked with the same value it returns and it says 

**Group theory is fun**

`ansperm` is a cryptic to the phrase `answer of permutation`. Assuming this, lets continue reversing this permutation algorithm. Since its 7 indexed array, Since there's a lot of math, We'll solve this manually instead of automating. We know that the final solution has to be `9059178`

![heap2](https://github.com/purrate/4.PCTF24/assets/132884539/91f93aa3-8761-40e3-9788-67c69da13a70)

![heap1](https://github.com/purrate/4.PCTF24/assets/132884539/c281068a-af6a-4147-9e1b-7e587674cee6)

As we are generating permutations of this array, We can start seeing that this algorithm seems very similar to the Heap's algorithm of generating permutations. 

<Heap Wikipedia><img width="877" alt="heappermwiki" src="https://github.com/purrate/4.PCTF24/assets/132884539/0f29bb60-754a-4bdb-b71a-af84fa58648f">


<img width="101" alt="heapperm" src="https://github.com/purrate/4.PCTF24/assets/132884539/4d173021-cbc1-4478-aa7f-1cb9e42e5ef4">


<Heap code><img width="402" alt="heappermgfg" src="https://github.com/purrate/4.PCTF24/assets/132884539/fad1c425-28e2-434a-bea4-5ddf48732f31">

<img width="302" alt="heapsc" src="https://github.com/purrate/4.PCTF24/assets/132884539/52cb2f15-cbb0-4815-8f95-9b986e5b3aea">

We know that the `count` variable is 49 from the pervious process. So we have to find the number for which the 49th permutation is `9059178`. With a tedious bit of math and resilience (Or you can be smart and figure out that during the 49th permutation, first two digits dont change and just calculate the rest). We figure out that the original number is `9019578`

Now we know, `c[0] = 9, c[1] = 0, c[2] = 0, c[3] = 7, c[4] = 1, c[5] = 9, c[6] = 9, c[8] = 5, c[10] = 7, c[12] = 0, c[14] = 8, c[15] = 1`

## Process 4:

As we can see, We are gonna be working with another 4 digit number, Instead of reversing this algorithm, We'll replicate it and run it along all 4 digit numbers to check which number matches this final value. 

NOTE: The last element of the `sup` array isn't included in the operations below so it must be a red herring.

Let's do this

<img width="617" alt="finalsc" src="https://github.com/purrate/4.PCTF24/assets/132884539/3a9bb44c-2a3e-4620-b430-ff44def78f66">

The count variable is used to avoid the cases where the while loop goes on infinitely and we don't want to do that either way. When we run this program, We get the 4 digit number as `2448`

<img width="444" alt="process4re" src="https://github.com/purrate/4.PCTF24/assets/132884539/48fc9bea-89a6-47a3-8d4a-001906942deb">

Now, we know, `c[0] = 9, c[1] = 0, c[2] = 0, c[3] = 7, c[4] = 1, c[5] = 9, c[6] = 9,c[7] = 2, c[8] = 5, c[9] = 4, c[10] = 7, c[11] = 4, c[12] = 0, c[13] = 8, c[14] = 8, c[15] = 1`

We have finally figured out the first 16 digits of the number.

Its `9007199254740881`. But why this number ? Why would anyone use this number to "prank". Well this number is supposed to be the largest prime number that **javascript** can represent. (Its 2^53 - 1). We can spot that there's a recurrring theme of `prime` numbers considering this and the fact that `fermats little theorem` and `euclidean algorithm` were used to check for primality.

## Uknown Error

<img width="892" alt="dshufflesource2" src="https://github.com/purrate/4.PCTF24/assets/132884539/07c95aec-bb5b-4617-9ae6-6b807f43e8f8">

This subprocess is forming an array of size 8 called `second` and a variable `sed` is declared which is equal to 49823739. This calls the function `deterministicshuffle` inside a for loop that runs for 8 times. But we notice that we don't need to check all 8 iterations because we have another array inside the loop that checks if it's equal to the second array called `check`. So we only need to track the first 7 iterations and figure out the original positions of the array.

Now let's take a look at the deterministicshuffle function.

<img width="517" alt="dshufflesource" src="https://github.com/purrate/4.PCTF24/assets/132884539/416b30ef-1669-47f1-ad89-ea7357d311a3">

At first look, We can see that `srand()` and `rand` functions are used. But how can we reverse engineer a function that generates random integers ? Well, looking a the man page of `srand()`

` The srand() function sets its argument as the seed for a new sequence  of `
`       pseudo-random  integers  to  be  returned by rand().  These sequences are `
`       repeatable by calling srand() with the same seed value. `

Since we have the information on how the seed is generated and we know how srand() function works. It's easy to replicate the functionality of srand()

NOTE: You can also use gdb to decompile and check what value srand() produces in that certain binary. But for convenience purposes, We'll be using python's `ctypes` library and `CDLL` method to generate the random number sequences OR we can also use a simple C program to generate the sequence. 

We are gonna be working with a pseudo random number generator.

<img width="493" alt="srand" src="https://github.com/purrate/4.PCTF24/assets/132884539/95c506e5-2111-4e51-ac08-4584acf4c2b2">

We get the output as, 

rand : 1480414540
j is 4
rand : 2034542318
j is 4
rand : 714231434
j is 2
rand : 46929865
j is 0
rand : 133649075
j is 3
rand : 1580585121
j is 0
rand : 511071142
j is 0

rand : 1255255328
j is 0
rand : 1653139788
j is 6
rand : 410223537
j is 3
rand : 395787845
j is 0
rand : 1239535544
j is 0
rand : 124729213
j is 1
rand : 74589022
j is 0

rand : 1881621530
j is 2
rand : 259435078
j is 0
rand : 553878631
j is 1
rand : 1921326620
j is 0
rand : 1623068584
j is 0
rand : 278601346
j is 1
rand : 372195585
j is 1

rand : 241213472
j is 0
rand : 353325096
j is 5
rand : 744972345
j is 3
rand : 1922255747
j is 2
rand : 446737372
j is 0
rand : 174392692
j is 1
rand : 1697475877
j is 1

rand : 310501282
j is 2
rand : 1982105573
j is 0
rand : 819355572
j is 0
rand : 1127591413
j is 3
rand : 665821445
j is 1
rand : 1997600696
j is 2
rand : 1051912918
j is 0

rand : 1328633442
j is 2
rand : 11616408
j is 6
rand : 1292231073
j is 3
rand : 328371439
j is 4
rand : 802714656
j is 0
rand : 83446321
j is 1
rand : 318284795
j is 1

rand : 1026002385
j is 1
rand : 29045273
j is 5
rand : 1284448975
j is 1
rand : 1593323101
j is 1
rand : 1081170792
j is 0
rand : 1902028314
j is 0
rand : 1842226169
j is 1

rand : 991546732
j is 4
rand : 223689110
j is 1
rand : 1389920802
j is 0
rand : 512106112
j is 2
rand : 700484023
j is 3
rand : 1051442420
j is 2
rand : 67012877
j is 1

Ooph, That's a lot to reverse. Let's reverse it using a simple code. 

<img width="609" alt="srandre" src="https://github.com/purrate/4.PCTF24/assets/132884539/9823a796-d154-47d7-96f1-58999a102fab">

><img width="233" alt="srando" src="https://github.com/purrate/4.PCTF24/assets/132884539/7e930042-6571-4b5f-af51-834956050967">

As we can see, We've got the indices after permutation shuffling. Now, let's map it to the list of integers given in the `check` array to obtain the original second array. 

Now we know, `c[16] = 7, c[17] = 5, c[18] = 2, c[19] = 3, c[20] = 7, c[21] = 2, c[22] = 5, c[23] = 3`

## Process 5

<img width="528" alt="process5sc" src="https://github.com/purrate/4.PCTF24/assets/132884539/dddef398-70ba-4757-a51b-1a6a734d176e">

We are given 2 arrays `seed` and `cum`, But this time, As we can see We are gonna be working with a bunch of ASCII values instead of just the integer values obtained by the program. These values get put into a matrix called `mn` and this matrix undergoes another shifting algorithm using a constant srand() seed. This cracking should be much easier than the previous one. But let's make this crack even smarter. If u look at the array that it's being checked with after undergoing shuffling. We can see that the biggest number possible is a 4 digit number, Which makes sense because the minimum number that the `seed` or `cum` could be is 53328. This happens when all the characters are equal to '0'. 

But the weirder part is that we are only able to see only one 4 digit number which shouldn't be the case. Is the question unsolveable ???? Well, Not really. If you've been following closely. I think you might remember the weird thing that `fgets()` function does. It assigns space to a null character automatically to the end of the string when the input is taken it. This means the `seed` number is a 4 digit number by default since `c[31]` is taken in as NULL while the input is called. This makes sense now.

Instead of using the random number generator, We can be smart and bruteforce the characters. Since we know we are only gonna be using ASCII values of characters [0 - 9]. 

Let's checkout `cum` first:

<img width="690" alt="cum" src="https://github.com/purrate/4.PCTF24/assets/132884539/5e52df93-99d2-4356-be7a-ba841e251da0">

<img width="97" alt="cumo" src="https://github.com/purrate/4.PCTF24/assets/132884539/f301c786-8749-499a-8d60-17519e5d86e2">

As, we can see below, The first 3 numbers are confirmed to be 5 2 7. The last digit could be anything from 0 to 9.

Likewise, We figure out that the numbers for `seed` is also NULL 5 2

Now we know, `c[16] = 7, c[17] = 5, c[18] = 2, c[19] = 3, c[20] = 7, c[21] = 2, c[22] = 5, c[23] = 3, c[24] = 5, c[25] = 2, c[26] = 7, c[29] = 2, c[30] = 5`

## The Last Digit

<img width="619" alt="final" src="https://github.com/purrate/4.PCTF24/assets/132884539/6c102900-4d37-4386-b288-393b8f7c8759">

We know that the last digit that is `c[31]` is taken in as NULL character but the program says we need to input 32 characters. What could be the 32nd char. It's plainly given that its 7 at the end of the program. I'm very disappointed with this challenge for being so easy.

## Finishing Up

Still we have a few things that need to be fixed. Remember that we weren't able to figure out what c[27] and c[28] are. Which means the flag can have 99 different possible values. How can we find out which is the right flag ? Well we can reverese engineer the `matrix shuffle` function that's given at the top to figure out how shuffles are gonna work and what the last 2 characters are gonna be. It's gonna be much simpler now that we have figured out what `seed` and `cum` are. We can use these values and reverse engineer matrice `mn` to make it equal to the matrix `ab`. OR

If you've been closely following this challenge, There has been a lot of recurring pattern of prime numbers being the answers. We can make use of this fact and figure out that this number is also going to be a prime number. So far we have...

`75237253527__257`

16 digit prime numbers aren't that hard to find online. If you search up 16 bit prime numbers, You'll be able to find a number which is gonna closely match with this number and we get the last two digits as `33`

Finally the flag is gonna be `90071992547408817523725352733257`.
