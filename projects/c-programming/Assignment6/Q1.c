//
//  main.c
//  Assignment6(cs2004)
//
//  Created by Elliott Barnes on 2020-03-29.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//


#include<stdio.h>
#include<stdlib.h>
#include<pthread.h>
#include<unistd.h>

// shared memory

int sum = 0;
int r_val = 0;
int rw_flag = 1;

// prototypes

void *getinput(void *param);
void *calculatesum(void *param);
    
  

int main() {
    
    pthread_t tid[2];

    // create the read thread
    
    pthread_create(&tid[0], NULL, getinput, NULL);

    // create the sum thread
    
    pthread_create(&tid[1], NULL, calculatesum, NULL);

    // block getinput until calculatesum finishes
    
    pthread_join(tid[1], NULL);
    
    printf("Sum is %d\n", sum);

    return 0;

    
    
}

//first thread for input

void *getinput() {
    do {
        while(!rw_flag)
            
        sleep(1);

        sleep(1);

        // read value from input
        
        int val;
        
        printf("Enter a integer: ");
        
        scanf("%d", &val);
        
        // storing input in shared memory
        
        r_val = val;
        
        // set flag to resume sum thread
        
        rw_flag = 0;

        // exit if sentinel (negative) val entered
        
        if(val < 0) {
            pthread_exit(NULL);
        }
        
    } while(1); //infinite loop
}

void *calculatesum() {
  do {
      
      // wait till flag sets
      
      while(rw_flag)
      
      sleep(1);
      
      // read val from shared memory
      
      int val = r_val;

      // exit if sentinel (negative) val entered
      
      if(val < 0) {
      
      pthread_exit(NULL);
          
      }
      
      sum += val;
      
      // set flag to return to getinput
      
      rw_flag = 1;
      
  } while(1); //infinite loop
  }
