//
//  main.c
//  Q4
//
//  Created by Elliott Barnes on 2020-03-01.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//

#include <stdio.h>
#include <sys/types.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>



#define BUFFER_SIZE 25
#define READ_END 0
#define WRITE_END 1

int fd1[2], fd2[2];
pid_t pid;


int main(void) {
    char write_message[BUFFER_SIZE];
    printf("Enter a string (e.g., Hi There): ");
    fgets(write_message, sizeof(write_message), stdin);
    char read_message[BUFFER_SIZE];
    pipe(fd1);
    pipe(fd2);
    
    /* create the pipe */
    if (pipe(fd1) == -1) {
       fprintf(stderr,"Pipe failed");
    return 1;
    }
    /* fork a child process */
    pid = fork();
    if (pid < 0) {
        /* error occurred */
        fprintf(stderr, "Fork Failed");
        return 1;
    }
    if (pid > 0) {
        /* parent process */
    /* close the unused end of the pipe */
        close(fd1[READ_END]);

        /* write to the pipe */
        write(fd1[WRITE_END], write_message, strlen(write_message)+1);
           /* close the write end of the pipe */
        close(fd1[WRITE_END]);
        
        read(fd2[READ_END], read_message, BUFFER_SIZE);
        printf("\nNow i read: %s\n",read_message);
        close(fd2[READ_END]);
        }
    else {
        /* child process */
    /* close the unused end of the pipe */
        close(fd1[WRITE_END]);
    /* read from the pipe */
        read(fd1[READ_END], read_message, BUFFER_SIZE);
        
        printf("\nOriginal message: %s",read_message);
       /* close the read end of the pipe */
        close(fd1[READ_END]);
        /* Reverse case of chars in string*/
        for(int i=0;i<strlen(read_message);i++){
            if(read_message[i] >= 'A' && read_message[i] <= 'Z'){
                read_message[i] = tolower(read_message[i]);
            }
            else if (read_message[i]>= 'a' && read_message[i] <= 'z'){
                read_message[i] = toupper(read_message[i]);
            }
               }
        
        close(fd2[READ_END]);
        write(fd2[WRITE_END], read_message, strlen(write_message)+1);
        close(fd2[WRITE_END]);
        
    }
        

    

    
    return 0;
}
