all : mainFile execute

mainFile: Main.c 

		mpicc -o out Main.c bs.c wsn.c -lm

execute:

		mpirun -oversubscribe -np 26 out 5 5 5

clean : 

		rm alertlog.txt
		

