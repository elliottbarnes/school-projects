//
//  main.c
//  PidManager
//
//  Created by Elliott Barnes on 2020-02-08.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//

#include <stdio.h>

#include <stdlib.h>

#include <string.h>

#define MIN_PID 300

#define MAX_PID 5000

char *pid_map = NULL;

/* create data structure for representing pids*/

int allocate_map(void)

{
    
pid_map = (char *)malloc((MAX_PID-MIN_PID+1) * sizeof(char));

// return -1 if unsuccessful
    
if (pid_map == NULL)
return -1;

// return 1 if successful

memset((void *)pid_map, 0x0, MAX_PID-MIN_PID+1);
return 1;
    
}

/* method to allocate & represent pid*/

int allocate_pid(void)

{

// search for free space in map to allocate pid

int iter = 0;
for (iter = 0; iter <= MAX_PID-MIN_PID; iter++)

{
    
if (pid_map[iter] == 0)

{

pid_map[iter] = 1;
return MIN_PID + iter;

}

}

return -1;

}

/* method for releasing a pid*/

int release_pid(int pid)

{

// check to see if empty, if not release pid

if((pid >= MIN_PID) && (pid <= MAX_PID) && (pid_map[pid-MIN_PID] == 1))

{

pid_map[pid-MIN_PID] = 0;
return 1;

}

else

return -1;

/* main function */

}

int main()

{
    // implemented api with linux method / left blank because told it was a code review
}

}
