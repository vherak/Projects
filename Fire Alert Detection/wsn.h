#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>
#include <pthread.h> 

#ifndef SENSORNODES_H
#define SENSORNODES_H

int WSN_Nodes( MPI_Comm world_comm, MPI_Comm comm );

#endif