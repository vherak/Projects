#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <mpi.h>
#include <time.h>
#include <unistd.h>
#include <stdbool.h>
#include <pthread.h> 

#ifndef BASESTATION_H
#define BASESTATION_H

int baseStation( MPI_Comm world_comm, MPI_Comm comm, int rows,int cols,int nIteration);
void *ThreadFunc(void *pArg); // POSIX thread function format


#endif
