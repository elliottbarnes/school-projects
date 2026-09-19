//
//  q7.c
//  Q7
//
//  Created by Elliott Barnes on 2020-04-09.
//  Copyright © 2020 Elliott Barnes. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define REFSTRINGLEN 20

void generateData(void);
void fifo(void);
void opt(void);
void lru(void);

int  nf, p[50]; /* initialize global variables */
int ref_string[REFSTRINGLEN]; /* initialize reference string */

void generateData(){ // generate reference string
    
    srand(time(NULL));
    
    printf("Page reference string: ");
    for(int i = 0; i<20; i++){
        ref_string[i] = rand() % 10; /* fill reference string w 20 ints */
    }
    
    for(int i = 0; i<20; i++){
        printf("%d", ref_string[i]); /* print reference string */
    }
    printf("\n");
    
}

void fifo(void){ // execute fifo algorithm on reference string

    int i, num, x = 0, y = 0, z = 0, pfct = 0, flag = 0; /* initialize local vars for fifo */

     for (i = 0; i<nf; i++) /* initialize page frame */

     {

          p[i] = -1;

     }

     while (z<20)

     {

          flag = 0;

          num = ref_string[z];
         
          for (i = 0; i<nf; i++) /* check if number already in frame */

          {

              if (num == p[i])

              {

                   z++;

                   flag = 1;

                   break;

              }

          }

          if (flag == 0) /* if page isn't in frame*/

          {

              if (y<nf)

              {

                   p[y] = ref_string[z];
                   y++;
                   z++;
                   pfct++;

              }

              else

              {

                   if (x<nf)

                   {

                        p[x] = ref_string[z];
                        z++;
                        x++;
                        pfct++;

                   }

                   else
                       
                        x = 0;
              }

          }

          

          printf("\n");

          for (i = 0; i<nf; i++)

          {

              printf("%d\t", p[i]);

          
     }
     }

     printf("\nTotal Number of Page Faults (FIFO): %d\n", pfct);
}

void opt(void){
    int  i, j, k, x, y, op, flag, temp, max, a = 0, pfct = 0, tempFlag = 0, count[10]; /* initialize local vars for opt */

    for (i = 0; i<nf; i++){

        count[i] = 0;

        p[i] = -1;

        }

        for (i = 0; i<REFSTRINGLEN; i++)

        {

             flag = 0;

             temp = ref_string[i];

             for (j = 0; j<nf; j++) /* check if value is in page frame */

             {

                 if (temp == p[j])

                 {

                      flag = 1;

                      break;

                 }

             }

             if ((flag == 0) && (a<nf)) /* if page frame has free slot */

             {

                 pfct++;

                 p[a] = temp;

                 a++;

             }

             else if ((flag == 0) && (a == nf)) /* if page frame is full */

             {

                 pfct++;

                 for (k = 0; k<nf; k++)

                 {

                      count[k] = 0;

                 }

                 for (x = 0; x<nf; x++) /* opt replacement */

                 {

                      tempFlag = 0;

                      for (y = i + 1; y<REFSTRINGLEN; y++)

                      {

                           if (p[x] == ref_string[y])

                           {

                                if (count[x] == 0)

                                     count[x] = y;

                                tempFlag = 1;

                           }

                      }

                      if (tempFlag != 1)

                      {

                           count[x] = REFSTRINGLEN + 1;

                      }

                 }

                 op = 0; /* find opt page */

                 max = count[0];

                 for (k = 0; k<nf; k++)

                 {

                      if (count[k]>max)

                      {

                           max = count[k];

                           op = k;

                      }

                 }

                 p[op] = temp;

             }


             printf("\n");

             for (k = 0; k<nf; k++)

             {

                 printf("%d\t", p[k]);

             }

        }

        printf("\nTotal Number of Page Faults (OPT): %d\n", pfct);

}

void lru(){
   int  i, j, x, y, z, flag, temp, least,  k = 0, pfct = 0, count[10];

     for (i = 0; i<nf; i++)

     {

          count[i] = 0;

          p[i] = -1;

     }

     for (i = 0; i<20; i++)

     {

          flag = 0;

          temp = ref_string[i];

          for (j = 0; j<nf; j++) /* check if page in frame */

          {

              if (temp == p[j])

              {

                   flag = 1;

                   count[j] = i;

                   break;

              }

          }

          if ((flag == 0) && (k<nf)) /* if the page isn't in frame & frame has free slot*/

          {

              pfct++;

              p[k] = temp;

              count[k] = i;

              k++;

          }

          else if ((flag == 0) && (k == nf)) /* if the page isn't in frame & frame has free slot */

          {

              pfct++;

              least = count[0]; /* find most recently used page */

              for (z = 0; z<nf; z++)

              {

                   if (count[z]<least)

                   {

                        least = count[z];

                        y = z;

                   }

              }

              p[y] = temp;

              count[y] = i;

              y = 0;

          }

          
         
          printf("\n");

          for (x = 0; x<nf; x++)

          {

              printf("%d\t", p[x]);

          }

     }

     printf("\nTotal number of Page Faults (LRU): %d\n", pfct);

}

int main() {
    // insert code here...
    printf("Enter number of Frames: ");
    scanf("%d", &nf);
    generateData();
    fifo();
    opt();
    lru();
    return 0;
}
