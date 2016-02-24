#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <time.h>
#define TICS 1
#define WINDOW 10
#define DEBUG 0
#define CPUS 1
#define ACTIVE_TRSH 20

typedef struct node{
	struct node *next;
	float value;
}nd;

typedef struct time_series{
	struct node *head;
	struct node *end;
	int size;
}ts;

float simple_average(ts *t){
	float sum=0.0;
	int cont=0;
	nd *aux;
	aux=t->head;
	if(!aux) return(0.0);
	while(aux->next){
		sum+=aux->value;
		cont++;
		aux=aux->next;
	}
	return(sum/cont*1.0);
}

float activetime(ts *t){
	int i;
	int cont=0;
	nd *aux;
	aux=t->head;
	if(aux==NULL) return(0.0); 
	while(aux->next!=NULL){ 
		if(aux->value>=ACTIVE_TRSH){
			cont++;
		}
		aux=aux->next;
	}
	return(cont*1.0/t->size);

}

float wheighted_average(ts *t){
	float sum=0.0;
	int cont=0;
	int sumCount=0;
	nd *aux;
	aux=t->head;
	if(!aux) return(0.0);
	while(aux->next){
		cont++;
		sum+=aux->value*cont;
		aux=aux->next;
		sumCount+=cont;
	}
	return(sum/sumCount*1.0);
}

void enqueue(ts *t, float data){
	nd *aux;
	aux = (nd *)malloc(sizeof(nd));
	aux->value=data;
	aux->next=NULL;
	if(t->end){
		t->end->next=aux;
		t->end=aux;
	}
	else{
		t->head=aux;
		t->end=aux;
	}
	t->size+=1;
}

void dequeue(ts *t){
	nd *aux;
	if(t->head){
		aux=t->head;
		t->head=aux->next;
		free(aux);
		t->size-=1;
	}
	else{
		return;
	}
}

void initialize(ts *t){
	t->size=0;
	t->head=NULL;
	t->end=NULL;
}

int size(ts *t){
	return(t->size);
}

char command[256], temp[20];
char *mode = "r";
FILE *file, *ifp;

long int cpu_usage, cpu_usage_prev=9999999, active_duration=0;
float cpu_usage_perc;
float queue,kernel_queue;
//float cpu_time_series[WINDOW];
//float queue_time_series[WINDOW];
float guiltiness;
float active_time_percent;
float queue_average,queue_average_wheighted;
float kernel_queue_average,kernel_queue_average_wheighted;
//int cont=0;
int flag=1,flag_window=0;

float average(float *vet, int size){
	int i;
	float sum=0.0;
	for(i=0;i<size;i++) sum+=vet[i];
	return(sum/size);
}


/*

float activetime(float *vet, int size){
	int i;
	int cont=0;
	for(i=0;i<size;i++) {
		if(vet[i]>=20.0){
			cont++;
		}
	}
	return(cont*1.0/size);
}*/



main(int argc, char **argv){

	system("rm -r tmp log");
	system("mkdir tmp log");
	int i;
	int cont=0;
	ts cpu_time_series,queue_time_series, kernel_queue_time_series;
	initialize(&cpu_time_series);
	initialize(&queue_time_series);
	initialize(&kernel_queue_time_series);
	//time series initialization
	/*for(i=0;i<WINDOW;i++) {
		cpu_time_series[i]=0;
		queue_time_series[i]=0;
	}*/

	while(1){

		if(cont>=WINDOW){
			flag_window=1;
		} 
		if(flag_window==1){

			dequeue(&cpu_time_series);
			dequeue(&queue_time_series);
			dequeue(&kernel_queue_time_series);
		}

		//CPU UTILIZATION
		//system("mpstat 1 1 | grep age | awk {' print 100-$11 '} | tee tmp/cpu-usage >> log/cpu-usage");
		//sprintf(command,"/sys/fs/cgroup/cpuacct/%s/cpuacct.usage",argv[1]);
		system("cat /proc/stat | grep cpu | head -n 1 | awk {' print $5 '} | tee tmp/cpu-usage >> log/cpu");
		sprintf(command,"tmp/cpu-usage");

		ifp = fopen(command,mode);
        if (ifp ==NULL) printf("ERROR IN OPEN CPU USAGE FILE");
        fscanf(ifp,"%ld",&cpu_usage);
       	fclose(ifp);
       	
		if(flag == 1) {// if is the first iteration
			cpu_usage_prev=0; 
			flag = 0;
		}
		//cpu_usage=(cpu_usage-cpu_usage_prev)/TICS;
		cpu_usage_perc=100-(cpu_usage-cpu_usage_prev)/(CPUS*1.0);
		if(cpu_usage_perc<0) cpu_usage_perc=0.0;

		enqueue(&cpu_time_series,cpu_usage_perc);
		//cpu_time_series[cont]=cpu_usage_perc;

		sprintf(command,"echo %f >> log/cpu-usage",simple_average(&cpu_time_series));
		system(command);

		active_time_percent=activetime(&cpu_time_series);
	

		sprintf(command,"echo %f >> log/activetime",active_time_percent);
		system(command);

		if(DEBUG) printf("------------------\nCPU Active time: %f\n\n", active_time_percent);
		if(DEBUG) printf("CPU TIME: %ld CPU TIME PREVIOUS: %ld RESULT: %ld\n", cpu_usage,cpu_usage_prev,cpu_usage-cpu_usage_prev);
		if(DEBUG) printf("CPU: %f\n", cpu_usage_perc);
		if(DEBUG) printf("CPU Moving Average: %f\n", simple_average(&cpu_time_series));
		if(DEBUG) printf("CPU WMA: %f\n", wheighted_average(&cpu_time_series));
		if(DEBUG) printf("TIME SERIES SIZE: %d\n", size(&cpu_time_series));


		cpu_usage_prev=cpu_usage;
        	//Compute active duration times
        	//The active duration is the time interval between two idle states
        if(cpu_usage_perc <= ACTIVE_TRSH && active_duration>0){
        	// The VM is in now in idle state
        	sprintf(command,"echo %ld >> log/active-duration",active_duration);
    		system(command);
    		active_duration=0;
        }
        else{
        	active_duration+=1;
        	//sprintf(command,"echo %ld >> log/active-duration",active_duration);
    		//system(command);
        }
		//QUEUE BACKLOG
		
		sprintf(command,"tc -s -d qdisc show dev eth0 | grep backlog | awk {' print $2 '} | sed \'s/b//\' | tee tmp/queue >> log/queue");
  		system(command);
  		sprintf(command,"tail -n 1 log/kernel-queue > tmp/kernel-queue"); 
  		system(command);
    	//netstat -untpa |  awk '{Queue += $3; } END {  print Queue }'
    	//sprintf(command,"netstat -untpaw |  | tee tmp/queue >> log/queue");
    	
		//COMPUTAR O VETOR DA FILA
		sprintf(command,"tmp/queue");
    	ifp = fopen(command,mode);
        if (ifp ==NULL) printf("ERROR IN OPEN QUEUE FILE");
        fscanf(ifp,"%f",&queue);
       	fclose(ifp);
       	if(DEBUG) printf("QUEUE: %f\n", queue);
       	if(queue>0) enqueue(&queue_time_series,queue);
       	else enqueue(&queue_time_series,0);
       	//queue_time_series[cont]=queue;

       	sprintf(command,"tmp/kernel-queue");
    	ifp = fopen(command,mode);
        if (ifp ==NULL) printf("ERROR IN OPEN KERNEL QUEUE FILE");
        fscanf(ifp,"%f",&kernel_queue);
       	fclose(ifp);
       	if(DEBUG) printf("KERNEL QUEUE: %f\n", kernel_queue);
       	if(queue>0) enqueue(&queue_time_series,kernel_queue);
       	else enqueue(&queue_time_series,0);

       	queue_average=simple_average(&queue_time_series);
       	queue_average_wheighted=wheighted_average(&queue_time_series);

       	kernel_queue_average=simple_average(&kernel_queue_time_series);
       	kernel_queue_average_wheighted=wheighted_average(&kernel_queue_time_series);

       	sprintf(command,"echo %f >> log/queue-moving-average",queue_average);
    	system(command);
    	
       	sprintf(command,"echo %f >> log/queue-moving-average",queue_average_wheighted);
    	system(command);

    	sprintf(command,"echo %f >> log/kernel-queue-moving-average",kernel_queue_average);
    	system(command);
    	
       	sprintf(command,"echo %f >> log/kernel-queue-moving-average",kernel_queue_average_wheighted);
    	system(command);
    	

    	if(DEBUG) printf("QUEUE Moving Average: %f\n", queue_average);
    	if(DEBUG) printf("QUEUE WMA: %f\n", queue_average_wheighted);
    	guiltiness=-0.88*(active_time_percent/(1+queue_average))+1.02*active_time_percent+0.0000014*queue_average;
    	if(guiltiness>1.0) guiltiness=100;
    	else guiltiness=guiltiness*100;
    	if(DEBUG) printf("GUILTINESS: %f\n", guiltiness);
    	sprintf(command,"echo %f >> log/guiltiness",guiltiness);
		system(command);


    	if(flag_window==0) {
    		cont++;
    		
    	}
		sleep(TICS);
	}

}
