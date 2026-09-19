//
//  main.c
//  q7
//
//  Created by Elliott Barnes on 2020-04-03.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//

#include<stdio.h>
#include<stdlib.h>

int main(int argc, char **argv)
{
    // defining page size (4kb)
    
   const int PAGE_SIZE = 4096;

   // variable to hold addr
    
   unsigned int addr_ref;

   // variable holding page number of the given address
    
   unsigned int page_number;

   // variable holding page offset of the given address
    
   unsigned int page_offset;

   // error check, arguments must be greater or equal to 2
    
   if (argc < 2)
   {
       
       printf("Atleast 2 arguments must be passed.\n");

       return -1;
       
   }

   // read val from userInput, convert string-int, store in addr variable
    
   addr_ref = atoi(argv[1]);

   // compute page number
    
   page_number = addr_ref / PAGE_SIZE;

  // compute page offset

   page_offset = addr_ref % PAGE_SIZE;

   // print addr, page number and page offset
    
   printf("The address %d contains:\n", addr_ref);
   printf("Page Number = %d\n", page_number);
   printf("Offset = %d\n", page_offset);

   return 0;
}
