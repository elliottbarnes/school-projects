//
//  main.c
//  Q3
//
//  Created by Elliott Barnes on 2020-03-15.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//

#include<unistd.h>
#include<stdio.h>
#include<time.h>
#include<stdlib.h>
#include<pthread.h>
#define MIN_PID 300
#define MAX_PID 5000
#define NUM_THREADS 100
#define YES 0
#define NO 1
pthread_mutex_t mutexV;

struct PidTable{
        int PID;
        int isFree;
}*pId;

int allocate_map(){
        int i;
        pId=(struct PidTable *)calloc((MAX_PID-MIN_PID+1),sizeof(struct PidTable));
        if(pId==NULL)
                return -1;
        pId[0].PID=MIN_PID;
        pId[0].isFree=YES;
        for( i=1;i<MAX_PID-MIN_PID+1;i++){
        pId[i].PID=pId[i-1].PID+1;
          pId[i].isFree=YES;
        }
        return 1;
}
int allocate_pid(){
   int i ;
   for( i=0;i<MAX_PID-MIN_PID+1;i++){
                if(pId[i].isFree==YES){
                        pId[i].isFree=NO;
                        return pId[i].PID;
                }
   }
        return -1;
}
void release_pid(int pid){
        pId[pid-MIN_PID].isFree=YES;
}


void *processStart(void *id){
        
        int pid,runTime;
        pthread_mutex_lock(&mutexV);
        pid=allocate_pid();
        usleep(100000);
        pthread_mutex_unlock(&mutexV);
        if(pid!=-1){
                
                printf("process allocated pid= %d \n",pid);
                runTime=rand()%10+1;
                printf("run time for process %d is %d\n",pid,runTime);
                sleep(runTime);
                printf("process %d releasing pid \n",pid);
                release_pid(pid);
        }
        pthread_exit(NULL);
}
int main(){
  allocate_map();
  srand(time(NULL));
  void *status;long i;
  int ret=0;pthread_t thread[100];
  pthread_mutex_init(&mutexV,NULL);
  for(i=0;i<NUM_THREADS;i++){
        ret=pthread_create(&thread[i],NULL,processStart,(void *)(i+1));
        if(ret){printf("error\n");exit(1);}
  }
  pthread_exit(NULL);
  pthread_mutex_destroy(&mutexV);
  return 0;
}
