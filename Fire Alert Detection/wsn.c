#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>
#include "wsn.h"
#include <pthread.h> 



#define SHIFT_ROW 0
#define SHIFT_COL 1
#define DISP 1
#define MSG_NO_EVENT 1
#define MSG_EVENT 2
#define NODE_EXIT 3


// declaring the lower and upper bound of the random temperatures being generated
int upper_bound = 90;
int lower_bound =75;


int WSN_Nodes( MPI_Comm world_comm, MPI_Comm comm ){

	/*
		This function simulates WSN Nodes and how we can detect a temperature anomaly. each process is 
		represented as one node in the grid. A cartesian topology is used to create the grid. If a temperature is 
		exceeding a certain threshold, we will check the adjacent nodes temperatures. If more than 2 is within a
		certain tolerance range, we will then send an alert to the base station. The sensor nodes keep on
		running until we receive a termination signal from the base station.

		parameters:
			world_comm: world communicator
			comm: communicator we are using to create the cartesian topology
	*/
    int ndims=2, size, my_rank, reorder, my_cart_rank, ierr, worldSize;
    int dims[ndims],coord[ndims];
	int wrap_around[ndims];
	int adjacent_nodes[4];
	int threshold = 80;

	MPI_Comm comm2D;

	MPI_Comm_size(world_comm, &worldSize); // size of the world communicator
    MPI_Comm_size(comm, &size); // size of the nodes communicator
    MPI_Comm_rank(comm, &my_rank);  // rank of the slave communicator

	dims[0]=dims[1]=0;
    MPI_Dims_create(size, ndims, dims);

	/* create cartesian mapping */
	wrap_around[0] = 0;
	wrap_around[1] = 0;
	reorder = 1;
	ierr = 0;

	// Creates the cartesian topology
	ierr = MPI_Cart_create(comm, ndims, dims, wrap_around, reorder, &comm2D);
	if(ierr != 0) printf("ERROR[%d] creating CART\n",ierr);


	/* find my coordinates in the cartesian communicator group */
	MPI_Cart_coords(comm2D, my_rank, ndims, coord); // coordinated is returned into the coord array

	/* use my cartesian coordinates to find my rank in cartesian group*/
	MPI_Cart_rank(comm2D, coord, &my_cart_rank);

	// gets adjacent nodes and stores them in an array
	MPI_Cart_shift( comm2D, SHIFT_ROW, DISP, &adjacent_nodes[0], &adjacent_nodes[1]);
	MPI_Cart_shift( comm2D, SHIFT_COL, DISP, &adjacent_nodes[2], &adjacent_nodes[3]);

	// creates arrays for send and receive status and requests
	MPI_Request send_request[4];
    MPI_Request receive_request[4];
    MPI_Status send_status[4];
    MPI_Status receive_status[4];

    int recvSignal = 0;

	// the sensor nodes will keep looping until they receive and exit message from the base station
    while(1){

		// sleeps for 1 second so that we can generate differnt random numbers
		sleep(1);
	    unsigned int seed = time(NULL)^my_rank;
        int randomTemperature=0;

		// generates a random temperature
    	randomTemperature = (rand_r(&seed) % (upper_bound-lower_bound+1)) + lower_bound ;

		// creates an array for the temperatures we received from the adjacent nodes
	    int receivedTemperatures[4];

	    // sends the temperature number of the current rank to the top,bottom,left and right ranks.
	    for(int i=0;i<4;i++)
	    {
		    // send random Temperature to every adjacent processor
		    MPI_Isend(&randomTemperature, 1, MPI_INT, adjacent_nodes[i], 0 , comm2D, &send_request[i]);

	    }

	    // receives the temperature of the left,right,top and bottom ranks and stores them
	    // in a list.
	    for(int i=0;i<4;i++)
	    {
			// receives Temperature from every adjacent processor
		    MPI_Irecv(&receivedTemperatures[i], 1, MPI_INT, adjacent_nodes[i], 0, comm2D,&receive_request[i]);
	    }

	    // waits for all mpi requests to complete
	    MPI_Waitall(4, send_request, send_status);
	    MPI_Waitall(4, receive_request, receive_status);

        
	    int counter = 0;
	    int tolerance = 5;

		// checks whether temperature is above the threshold. If it is, we will check whether the
		// adjacent nodes' temperature is within the tolerance range
	    if (randomTemperature > threshold){
	        for(int i=0; i<4; i++)
	        {
				// if adjacent nodes are within the tolerance range, we will increase the counter
	            if (abs(receivedTemperatures[i] - randomTemperature) <= tolerance && adjacent_nodes[i] != -2)
	            {
	                counter ++;
	            }
	        }
	    }

        // initializing buffer so we can pack the data to send to the base station
	    char buffer[1000];
	    int buffer_position=0;
	    int outputCount = 1000;
		float timer;
		float eventStart = MPI_Wtime();

		// if more than 2 adjacent nodes are within the tolerance range, and 'event' has happened
	    if (counter >= 2)
	    {   
	       printf("Event happened, Rank: %d,Temp: %d\n",my_rank,randomTemperature);
            timer = (int)time(NULL);

			// Pack the event start time
			MPI_Pack(&eventStart, 1, MPI_FLOAT, buffer, outputCount, &buffer_position, world_comm);

			// packs the times
            MPI_Pack(&timer, 1, MPI_FLOAT, buffer, outputCount,&buffer_position,world_comm);

            //packs the current rank
            MPI_Pack(&my_rank, 1, MPI_INT, buffer, outputCount,&buffer_position,world_comm);

            // packs the current ranks temperature
            MPI_Pack(&randomTemperature, 1, MPI_INT, buffer, outputCount,&buffer_position,world_comm);

            // packs the adjacent nodes temperatures
            MPI_Pack(receivedTemperatures, 4, MPI_INT,buffer,outputCount, &buffer_position, world_comm);

			// packs the adjacent nodes counter (how many nodes are within the tolerance range)
            MPI_Pack(&counter, 1, MPI_INT, buffer, outputCount,&buffer_position,world_comm);

            // packs the adjacent nodes ranks
            MPI_Pack(adjacent_nodes,4,MPI_INT,buffer,outputCount, &buffer_position, world_comm);

			// sends the buffer to the last process which is the base station
            MPI_Send(buffer, outputCount, MPI_PACKED, worldSize-1, MSG_EVENT, world_comm);
            //MPI_Send(buffer, 0, MPI_CHAR, worldSize-1, MSG_EVENT,world_comm);

	    }
		else{
			// If no event happened, we will send a NO_EVENT tag to the base station
			MPI_Send(buffer,outputCount,MPI_PACKED,worldSize-1,MSG_NO_EVENT,world_comm);
		}


    MPI_Request recvReq[1];
    MPI_Status status2;

	// Receives signal from the base station. If signal = 5, it means we do not stop yet.
	// If signal is 3, it means we need to stop the loop
    MPI_Recv(&recvSignal,1,MPI_INT,worldSize-1,NODE_EXIT,world_comm,&status2);

	// checking if the received signal is 3, meaning we need to stop
    if(recvSignal == 3)
    {
        break;
    }

    }
	MPI_Comm_free( &comm2D );
	return 0;

}
