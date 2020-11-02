randmain: randmain.o randcpuid.o
	$(CC) $(CFLAGS) -o randmain randmain.o randcpuid.o -ldl -Wl,-rpath=$PWD

randmain.o: randmain.c
	$(CC) $(CFLAGS) -c randmain.c

randcpuid.o: randcpuid.c
	$(CC) $(CFLAGS) -c randcpuid.c

randlibhw.so: randlibhw.c
	$(CC) $(CFLAGS) -fPIC -c randlibhw.c -o randlibhw.o
	$(CC) $(CFLAGS) -shared randlibhw.o -o randlibhw.so

randlibsw.so: randlibsw.c
	$(CC) $(CFLAGS) -fPIC -c randlibsw.c -o randlibsw.o
	$(CC) $(CFLAGS) -shared randlibsw.o -o randlibsw.so
