#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<time.h>
#include<pthread.h>
#include<semaphore.h>
#define MIN_PID 300
#define MAX_PID 5000
#define NUM_THREADS 100
#define YES 0
#define NO 1
sem_t SEM;

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
        long tid=(long)id;
        int pid,runTime;
        sem_wait(&SEM);
        pid=allocate_pid();
        sleep(10000);
        sem_post(&SEM);
        if(pid!=-1){
                
                printf("New Process Allocated Pid= %d \n",pid);
                runTime=rand()%10;
                sleep(runTime);
                printf("Process %d releasing pid \n",pid);
                release_pid(pid);
        }
        pthread_exit(NULL);
}
int main(){
  allocate_map();
  srand(time(NULL));
  void *status;
  int i;
  int ret=0;
  pthread_t thread[100];
  sem_init(&SEM,0,1);
  for(i=0;i<NUM_THREADS;i++){
        ret=pthread_create(&thread[i],NULL,processStart,(void *)(i+1));
        if(ret){printf("ERROR\n");exit(1);}
  }
  for(i=0; i<NUM_THREADS; i++) {
      ret = pthread_join(thread[i], &status);
      if (ret) {
         printf("ERROR; return code is %d\n", ret);
         exit(-1);
         }
  }
  return 0;
}