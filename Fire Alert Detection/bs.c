#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include "bs.h"
#include <unistd.h>
#include <stdbool.h>
#include <pthread.h> 

#define SHIFT_ROW 0
#define SHIFT_COL 1
#define DISP 1
#define MSG_NO_EVENT 1
#define MSG_EVENT 2
#define NODE_EXIT 3
#define SENTINEL 4816

// declaring global variables

int coordinate_limit_row = 3;
int coordinate_limit_col = 3;

int infraredSize = 5;
int infrared_list[4][4];
pthread_mutex_t g_Mutex = PTHREAD_MUTEX_INITIALIZER;

int baseStation( MPI_Comm world_comm, MPI_Comm comm, int rows,int cols,int nIteration){
	/*
	This function is the base station. Only the last process is the base station. The base station will
	create a thread which will simulate the infrared imaging satelite by periodically generating random
	coordinates and temperatures to compare with when we receive an alert from the sensor nodes. If all the
	conditions are met, we will then classifiy it as a true alert. If not, it will be classified as a false
	alert. It is then logged to a file. The base station will run a specific number of iterations unless
	stopped by the sentinel value which can be written in a text file by the user if they choose to stop it.
	After all the iterations are over, the base station will sending a terminating signal to all WSN nodes and
	the thread to stop running.

	Parameters:
		world_comm: world communicator
		comm: communicator

	*/

		// initializing all required variables
        int i, size;
        MPI_Status status;
        MPI_Comm_size(world_comm, &size );
        int nodes_num = size - 1;
	    char recv_buffer[1000];
		char buffer[256];
	    int outputSize = 1000;
	    float timer;
	    int position=0;
	    int main_rank=0;
	    int main_temp=0;
	    int adjacent_temp[4] ={0,0,0,0};
	    int adjacent_ranks[4]={0,0,0,0};
	    coordinate_limit_row = rows;
	    coordinate_limit_col = cols;
	    int signal = 0;
		int random = 1;
	    int curr_coord[2];
        int tolerance = 5;
        int column = cols;
		int trueAlertCounter;
		int adjacentCount;
		float eventStart;
		int totalEvent = 0;
		pthread_t tid;
		int worldSize;
		int arr[nIteration];
		int arrCount = 0;
		
		// initializng the array
		for(int i=0; i<nIteration;i++){
			arr[i] = 0;
		}

	    MPI_Comm_size(world_comm, &worldSize); // size of the world communicator
	    
	    // create the mutex
	    pthread_mutex_init(&g_Mutex, NULL);
	    
	    // creating the thread
	    pthread_create(&tid, 0, ThreadFunc, &worldSize);
	    sleep(1);

		// Log Files
		FILE * fp;  // pointer to the log file
		char *filename = "log.txt";
		/*create new file,give it a name and open it in binary mode  */
		fp = fopen(filename, "w"); /* w -  write mode */

    trueAlertCounter = 0; // to count the number of true alerts

	// runs a specific number of iterations
	for (int q=0; q< nIteration; q++){
		nodes_num = size - 1;
		arrCount = 0;

		// open the sentinel value file 
		int terminateValue;
    	FILE *fptr;

		// Program exits if file pointer returns NULL.
    	if ((fptr = fopen("terminateFile.txt", "r")) == NULL) {
        	printf("Error! opening file");
			break;
		}
        
		// reads text until newline is encountered
    	fscanf(fptr, "%d\n", &terminateValue);

		// if the number is 4816, it will terminate the program
    	if (terminateValue == SENTINEL){
    	    fclose(fptr);
    	    printf("User terminating the program..\n");
    	    break;
    	}
    	fclose(fptr);
    
		// prints formatting to log file:
        fprintf(fp, "=============================== Start of Iteration %d ===============================\n", q+1);
		
		// while all the node have not sent their event tags to the base station:
		while(nodes_num > 0){

			// receives the buffer from nodes
			MPI_Recv(recv_buffer,outputSize,MPI_PACKED,MPI_ANY_SOURCE,MPI_ANY_TAG,world_comm,&status);
			nodes_num --; 
			
			// if the node sent an event tag, we will unpack the items sent from the buffer
			if (status.MPI_TAG == MSG_EVENT){
				totalEvent += 1;

				// Mutex lock here to start comparing the temperature generated by infrared imaging satelitte
				pthread_mutex_lock(&g_Mutex); 
				
				// Unpack all the value here

				// unpacks the event start time to get the communication time
				MPI_Unpack(recv_buffer,outputSize,&position,&eventStart,1,MPI_FLOAT,world_comm);

				// unpacks the timer
	            MPI_Unpack(recv_buffer,outputSize,&position,&timer,1,MPI_FLOAT,world_comm);

				// unpacks the process that sent the alert
				MPI_Unpack(recv_buffer,outputSize,&position,&main_rank,1,MPI_INT,world_comm);

				// unpacks the processes temperature
				MPI_Unpack(recv_buffer,outputSize,&position,&main_temp,1,MPI_INT,world_comm);

				// unpacks the adjacent nodes temperature
				MPI_Unpack(recv_buffer,outputSize,&position,&adjacent_temp,4,MPI_INT,world_comm);

				// unpacks the number of adjcacent nodes that was in the tolerance range
				MPI_Unpack(recv_buffer,outputSize,&position,&adjacentCount,1,MPI_INT,world_comm);

				// unpacks the adjacent nodes ranks (process number)
				MPI_Unpack(recv_buffer,outputSize,&position,&adjacent_ranks,4,MPI_INT,world_comm);

				curr_coord[0] = main_rank / column; // get the coordinate from the current rank
				curr_coord[1] = main_rank % column; // get the coordinate from the current rank

				// Outputs to a file
				fprintf(fp,"\n");
				fprintf(fp, "---------------------------------------------------------------\n");
				fprintf(fp,"				Alert Summary %d in Iteration %d\n",trueAlertCounter,q+1);
				fprintf(fp, "---------------------------------------------------------------\n");
				time_t mytime = timer;
				char * time_str = ctime(&mytime);
				time_str[strlen(time_str)-1] = '\0';
				fprintf(fp,"Alert Reported Time:       %s\n",time_str);
				float eventEnds = MPI_Wtime();

				// gets the communication time by subtracting 
				float comTime = fabs(eventEnds - eventStart);
				fprintf(fp,"Communication Time: %f\n",comTime);
				fprintf(fp, "Reporting Node          Coord          Temp\n");

				// for printing purposes to make it look nice for 2 digits
				if (main_rank <= 9){
					fprintf(fp,"%d                       (%d,%d)           %d\n",main_rank,curr_coord[0],curr_coord[1],main_temp);	
				}
				else{
					fprintf(fp,"%d                      (%d,%d)           %d\n",main_rank,curr_coord[0],curr_coord[1],main_temp);
				}
				fprintf(fp,"\n");
				fprintf(fp, "Adjacent Nodes Temp     Coord          Temp\n");
				
				// if is adjacent node is outside the grid we will ignore it and not print on the log file
				for(int i=0;i<4;i++){
					if (adjacent_ranks[i] != -2){
					curr_coord[0] = adjacent_ranks[i] / column;
					curr_coord[1] = adjacent_ranks[i] % column;
					if (curr_coord[0] != -2 && curr_coord[1] != -2){
						if (adjacent_ranks[i] <= 9){
							fprintf(fp,"%d                       (%d,%d)           %d\n",adjacent_ranks[i],curr_coord[0],curr_coord[1],adjacent_temp[i]);
						}
						else{
							fprintf(fp,"%d                      (%d,%d)           %d\n",adjacent_ranks[i],curr_coord[0],curr_coord[1],adjacent_temp[i]);
						}
						
					}
					}
				}
				position = 0;

				// We will check whether the coordinates we received matched the coordinates in the infrared array
				fprintf(fp, "\n");
				int count = 0;
				for( int i = 0; i < infraredSize; i++){
					
					curr_coord[0] = main_rank / column;
					curr_coord[1] = main_rank % column;
					
					// if the time in between is smaller than 10 seconds
					if (infrared_list[i][3] - timer <= 10) {
						// if the infrared satellite coordinates is the same as the main coordinates
						if (infrared_list[i][1] == curr_coord[0] && infrared_list[i][2] == curr_coord[1]) {
							// if is within the tolerance, then make it true alert and upload to the file
							if (abs(main_temp - infrared_list[i][0]) <= tolerance){
								time_t mytime = time(NULL);
								char * time_str = ctime(&mytime);
								time_str[strlen(time_str)-1] = '\0';

								// prints to the log file
								fprintf(fp,"Infrared Satellite Reporting Time: %s\n", time_str);
								fprintf(fp,"Infrared Satellite Reporting (Celsius): %d\n",infrared_list[i][0]);
								fprintf(fp, "Infrared Satellite Reporting Coord: (%d,%d)\n",curr_coord[0],curr_coord[1]);
								fprintf(fp,"\n");
								count += 1;
								trueAlertCounter += 1;
								arrCount += 1;
								break;
								}
						}
					}
				}
				// If count is more than 0, it is a true aler
				if (count > 0){
					fprintf(fp,"Alert Type: True\n");
				}
				else{

					// If alert is classified as false alert, we will output the details to a file
					fprintf(fp,"Alert Type: False\n");
					for ( int i = 0; i < infraredSize; i++){
						time_t mytime = time(NULL);
						char * time_str = ctime(&mytime);
						time_str[strlen(time_str)-1] = '\0';
						fprintf(fp,"Infrared Satellite Reporting Time: %s\n", time_str);
						fprintf(fp,"Infrared Satellite Reporting (Celsius): %d\n",infrared_list[i][0]);
						fprintf(fp, "Infrared Satellite Reporting Coord: (%d,%d)\n",infrared_list[i][1],infrared_list[i][2]);
						fprintf(fp,"\n");
					}
				}				
				fprintf(fp,"Number of adjacent matches to reporting node: %d\n", adjacentCount);
				fprintf(fp,"\n");
				fprintf(fp,"\n");
				pthread_mutex_unlock(&g_Mutex); // unlock after finish comparing
			}
		}

		// If total events are 0, there were no alerts received in that iteration
		if (totalEvent == 0){
			fprintf(fp,"                                  --NO ALERT RECEIVE--                                    \n");
		}
		fprintf(fp, "=============================== End of Iteration %d ===============================\n\n", q+1);
		arr[q] = arrCount;
		fprintf(fp,"\n");

		// if is not the last iteration, send to the sensor node tell them to keep looping
		if (q != nIteration - 1){
			for (int i = 0; i < size-1; i++ ){
				// we will send the signal 5 to every node
				signal = 5;
				MPI_Send(&signal,1,MPI_INT,i,NODE_EXIT,world_comm);

			}
		}
	}

    signal = 3;
    // sends termination signal to all sensor nodes to stop the while loop;
    printf("Sending termination signal\n");

	// This is for the last iteration, we send exit signal to sensor nodes to break their own loop and exit
    for (int i = 0; i < size-1; i++ ){
        MPI_Send(&signal,1,MPI_INT,i,NODE_EXIT,world_comm);
    }
	sleep(1);
	printf("Base Station terminated\n");
        
	int exit = 1;

	// call the thread to exit
	MPI_Send(&exit,1,MPI_INT,worldSize-1,NODE_EXIT,world_comm);
		
	// Join the thread at the end of the process
	pthread_join(tid, NULL);
	
	pthread_mutex_destroy(&g_Mutex); // destroy the mutex

	fprintf(fp, "-------------------------End of Log-------------------------\n");
	fprintf(fp,"********* SUMMARY **********\n");
	fprintf(fp,"Total number of alerts: %d\n",totalEvent);
	fprintf(fp,"Total number of true alerts: %d\n",trueAlertCounter);
	fprintf(fp,"Total number of false alerts: %d\n",totalEvent - trueAlertCounter);
	for (i = 0; i < nIteration; i++){
     	fprintf(fp, "%d,", arr[i]);
	}
	fclose(fp);
	printf("Finish writing log file.\n");
    return 0;
}

void *ThreadFunc(void *pArg)
{	
	/*
	This function is the thread function that simulates the infrared imaging satelitte. It periodically
	generates random coordinates and temperatures until the base station tells it to stop. 

	*/

	// initialozes variables
	int exit = 0;
	int worldSize;
	MPI_Status status;
	int upper_bound = 90;
    int lower_bound =75;

	int* p = (int*)pArg;
	worldSize = *p;

	int tempCoordx;
	int tempCoordy;
	int counter;
	
	// runs in a while loop until base station tells it to stop
    while (1){
        MPI_Request request;

		// checks if base station sends an exit message
        MPI_Irecv(&exit, 1, MPI_INT, worldSize - 1, NODE_EXIT, MPI_COMM_WORLD, &request);
	
	    if (exit == 1){
	        break;
	    }
	        
	    else{   
            pthread_mutex_lock(&g_Mutex); // Mutex lock here to start comparing the temperature
			
	            for( int i = 0; i < infraredSize; i++){

	                // generates a random temperature
					unsigned int seed = time(NULL)^i;
                    int randomTemperature;
	                randomTemperature = (rand_r(&seed) % (upper_bound-lower_bound+1)) + lower_bound ;

	                //append in the infrared list
					infrared_list[i][0] = randomTemperature;
				
	                //generates a random coordinate and append in the infrared list
	                infrared_list[i][1] = (rand_r(&seed) % (coordinate_limit_row+1)) + 0 ;
                    infrared_list[i][2] = (rand_r(&seed) % (coordinate_limit_col+1)) + 0 ;
                    
					// generates the time
                    infrared_list[i][3] = (int)time(NULL);
                    
               }
			   // unlocks the mutex so the base station can use it               
                pthread_mutex_unlock(&g_Mutex);
	        }
	    
	    sleep(0.5); // pause awhile
	}
	printf("Thread terminated\n");
	return NULL;
}
