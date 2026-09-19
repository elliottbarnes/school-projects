//
//  main.c
//  Question7
//
//  Created by Elliott Barnes on 2020-01-29.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//

#include <stdio.h>

int main(int argc, const char * argv[]) {
    // insert code here...
    int b;
    int i = 1;
    printf("Enter an integer (1-200): ");
    scanf("%d", &b);
    if(b > 200 || b < 0)
    {
        printf("Value must be between (0-200)");
        printf("Enter an integer (0-200): ");
        scanf("%d", &b);
    }
    while(i <= b)
    {
        if(i % 3 == 0 && i % 5 != 0)
        {
            printf("three\n");
        }
        else if(i % 5 == 0 && i % 3 != 0)
        {
            printf("five\n");
        }
        else if((i % 3 == 0)&&(i % 5 == 0))
        {
            printf("threefive\n");
        }
        else
        {
            printf("%d\n", i);
        }
        
        i++;
    }
    
    return 0;
}
