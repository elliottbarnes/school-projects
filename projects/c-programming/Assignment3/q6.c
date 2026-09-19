//
//  main.c
//  FirstMultithreadedProgram
//
//  Created by Elliott Barnes on 2020-02-13.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int arr[50], i, j,sum, min, max, len;
int avg;


void *avg_number(void *value1)
{
    int *avg = (int *) value1;
     sum = 0;
    
    for(i = 0; i<len; i++){
        sum = sum + arr[i];
    }
    
    *avg = sum/len;
    printf("The average value is: %d\n", *avg);
    pthread_exit(0);
}

void *min_number(void *value2)
{
    int *min = (int *) value2;
    *min = arr[0];
    for(i = 0; i<len; i++){
        if(*min > arr[i]){
            *min = arr[i];
        }
            
        }
    printf("The minimum value is: %d\n", *min);
    pthread_exit(0);
    }

void *max_number(void *value3){
    
    int *max = (int *) value3;
    *max = arr[0];
    for(i = 0; i<len; i++){
        if(*max < arr[i]){
            *max = arr[i];
        }
            
        }
    printf("The maximum value is: %d\n", *max);
    pthread_exit(0);
}


int main(int argc, char ** argv) {
    pthread_t thread;
    pthread_t thread2;
    pthread_t thread3;
    
    printf("Enter how many integers are being calculated:");
    scanf("%d", &len);
    
    for(i=0; i< len; i++){
        scanf("%d", &arr[i]);
    }
    
    pthread_create(&thread, NULL, &avg_number, &avg);
    pthread_join(thread, NULL);
    pthread_create(&thread2, NULL, &min_number, &min);
    pthread_join(thread2, NULL);
    pthread_create(&thread3, NULL, &max_number, &min);
    pthread_join(thread3, NULL);
    return EXIT_SUCCESS;
    
}
