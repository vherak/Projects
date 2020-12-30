#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>
#include "bs.h"
#include "wsn.h"
#include <pthread.h> 

// to declare how many iterations the user wants to run
int nIteration =10;

int main(int argc, char *argv[]) {

	int ndims=2, size, my_rank, reorder, my_cart_rank, ierr;
	int nrows, ncols;
	int dims[ndims],coord[ndims];

	/* starting up the initial MPI environment */
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &size);
	MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
	MPI_Comm comm_new;
	MPI_Comm_split( MPI_COMM_WORLD,my_rank == size-1, 0, &comm_new);
	MPI_Status status;

	/* process command line arguments*/
	if (argc == 2){
		// getting the number of iterations
		nIteration = atoi (argv[1]);
	}
	if (argc == 4) {

		// getting input of rows and columns from the user
		nIteration = atoi (argv[1]);
		nrows = atoi (argv[2]);
		ncols = atoi (argv[3]);
		dims[0] = nrows; /* number of rows */
		dims[1] = ncols; /* number of columns */

		// prints error message if dimensions do not match the number of processes
		// we use size-1 as we need 1 processor for the base station
		if( (nrows*ncols) != size-1) {
			if( my_rank ==0) printf("ERROR: nrows*ncols)=%d * %d = %d != %d\n", nrows, ncols, nrows*ncols,size);
			MPI_Finalize(); 
			return 0;
		}

	} else {
		// gives default values using size if the user does not specify any
		nrows=ncols=(int)sqrt(size);
		dims[0]=dims[1]=0;
	}
	printf("Running sensor node %d now....\n",my_rank);

	// if the process is the base station (last process), run the base station function
	if (my_rank == size-1)
        baseStation( MPI_COMM_WORLD, comm_new,nrows,ncols,nIteration);
    else
	// if its a node, run the WSN nodes function
        WSN_Nodes( MPI_COMM_WORLD, comm_new );

    MPI_Finalize();
    return 0;
}
