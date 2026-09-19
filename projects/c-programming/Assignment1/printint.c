//
//  main.c
//  assignment1Revised(2005)
//  Question 6
//
//  Created by Elliott Barnes on 2020-01-28.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//

#include <stdio.h>

int main() {
    // insert code here...
    int n;
    int zeroDecrementer;
    int zeroCounter = 0;
    int arr[9];
    printf("Enter an integer (0-9 digits): ");
    scanf("%d", &n);
    while (n > 0) {
        int digit = n % 10;
        if(digit != 0)
        {
            arr[zeroCounter] = digit;
            //arr[freePos]=digit;
            //freePos +=1;
        }
        zeroCounter += 1;
        n /= 10;
    }
    zeroDecrementer = (zeroCounter - 1);
    for(int i = (zeroCounter-1); i >= 0 ; i--)
    {
        if(arr[i] != 0)
        {
            printf("%d", arr[i]);
            for(int j = zeroDecrementer; j > 0; j--)
            {
                printf("0");
            }
            zeroDecrementer -= 1;
            if(i == 0)
            {
                printf("\n");
                return 0;
            }
            printf(" ");
            printf("+");
            printf(" ");
        }
        else
        {
            zeroDecrementer -=1;
        }
        
        
    }
    
    return 0;
}
