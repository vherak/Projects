//---------------------------------------------------------------------------------------------------------------------
// PThreadSignalling.c
// Simulates communication between threads and main function when updating a shared variable
//---------------------------------------------------------------------------------------------------------------------
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#define NUM_THREADS 4

pthread_mutex_t g_Mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t g_Cond[NUM_THREADS] = {PTHREAD_COND_INITIALIZER};
int g_Val = 0; // Shared variable

void* ProcessFunc(void *pArg) // Common function prototype
{
	int* p = (int*)pArg;
	int myRank = *p; // Dereferences the pointer
	printf("Thread Id: %d\n", myRank);
	
	do{
		pthread_mutex_lock(&g_Mutex);
		pthread_cond_wait(&g_Cond[myRank], &g_Mutex);
		printf("Thread Id: %d. Global value: %d\n", myRank, g_Val);
		pthread_mutex_unlock(&g_Mutex);
	}while(g_Val >= 0);
	
	return 0;
}
 
int main()
{	
	pthread_t tid[NUM_THREADS];
	int threadNum[NUM_THREADS];
	int i = 0;
	printf( "Main process starts\n");
	
	// Initialize the mutex & condition variable
	pthread_mutex_init(&g_Mutex, NULL);

    	// Fork		
	for (i = 0; i < NUM_THREADS; i++)
	{
	    	threadNum[i] = i;
	    	pthread_cond_init(&g_Cond[threadNum[i]], NULL);
		pthread_create(&tid[i], 0, ProcessFunc, &threadNum[i]); // The third argument is the callback function
	}
	sleep(1);

	// Prompt value from user
	do{
		printf("Enter a round number (>= 0 ): ");
		fflush(stdout);
		pthread_mutex_lock(&g_Mutex);
		scanf("%d", &g_Val);
		pthread_mutex_unlock(&g_Mutex);
		
		// Wake up all threads
		for (i = 0; i < NUM_THREADS; i++){
			pthread_cond_signal(&g_Cond[i]);
		}
		sleep(1);
	}while(g_Val >= 0);
	
	
	// Join
	for(i = 0; i < NUM_THREADS; i++)
	{
	    	pthread_join(tid[i], NULL);
	}
	// All threads have safely been safely terminated
	
	// Clean up
	for (i = 0; i < NUM_THREADS; i++){
		pthread_cond_destroy(&g_Cond[i]);
	}
	pthread_mutex_destroy(&g_Mutex);
	printf( "Main process ends\n");
	return 0;
}