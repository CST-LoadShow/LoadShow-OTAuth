#include <jni.h>
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include "openssl/crypto.h"
#include "openssl/md5.h"
#include <android/log.h>
#include <openssl/aes.h>
#include <cstring>
#include <arpa/inet.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <openssl/rand.h>
#include <pthread.h>

#define N 16
#define M 64

using namespace std;
void fp_gen(uint64_t fp[N + 5][M + 5], int p, int chooseFunc);
char* send_fp(string device_label, uint64_t fp[N + 5][M + 5]);
void send_remote(char* res_char);
inline uint64_t as_nanoseconds(struct timespec* ts);


/** cpuid范围:[0,7] */
void cpu_affinity(int cpuid){
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(cpuid,&mask);
    if(sched_setaffinity(0,sizeof(cpu_set_t),&mask) < 0)
        printf("False: sched_setaffinity(0,sizeof(cpu_set_t),&mask)");
//        __android_log_print(ANDROID_LOG_ERROR, "False: sched_setaffinity(0,sizeof(cpu_set_t),&mask)");
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_fingerprint_NativeLib_getTimeFromJNI(
        JNIEnv* env,
        jclass clazz) {
//    /*=====================  test end ========================*/
//    __android_log_print(ANDROID_LOG_ERROR, "hellohello", "plain_text:");
//    struct timespec start, end;
//    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
//    // process
//    int cnt = 10000000;
//    while(cnt > 0){
//        cnt --;
//    }
//    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
//    float t = end.tv_nsec - start.tv_nsec;
//    __android_log_print(ANDROID_LOG_ERROR, "hellohellotimetime", "time:%f", t);
//    /*=====================  test end ========================*/

    string device_name;
    device_name = "Android device Google Pixel 4";

    uint64_t fp[N + 5][M + 5];
    int p = 500;
    int chooseFunc = 1;
    fp_gen(fp, p, chooseFunc);
    printf("Fingerprint generate success");
    char* ret_str = send_fp(device_name, fp);

    return env->NewStringUTF(ret_str);
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_fingerprint_NativeLib_getTimeFromOpenGL(
        JNIEnv* env,
jclass clazz) {
    // clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    return env->NewStringUTF("hello");
}

/**
 * 将 struct timespec 转换为 uint64_t 自纪元以来的纳秒数，并在它们之间取增量并轻松累加它们
 * */
inline uint64_t as_nanoseconds(struct timespec* ts) {
    return ts->tv_sec * (uint64_t)1000000000L + ts->tv_nsec;
}


uint64_t stall_function(long arg, int p){

    struct timespec start, end;
//    time_t time1 = (long)10;
//    srand(time(&time1));

    int* array = (int*) malloc(arg * sizeof(int));
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    for(int i = 0;i<p;i++) {
        for (int k = 0; k < arg; k++) {
            // int randomNumber = rand();
            uint32_t randomNumber = arc4random();
            array[k] = randomNumber;
         }
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    free(array);

    //long t = end.tv_nsec - start.tv_nsec;
    uint64_t t = as_nanoseconds(&end) - as_nanoseconds(&start);
    return t;
}

uint64_t stall_function_openssl(long arg, int p){
    struct timespec start, end;
    time_t time1 = (long)10;
    srand(time(&time1));

    int len = arg * sizeof(unsigned char);
    unsigned char* array = (unsigned char*)malloc(len);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    for(int i = 0;i<p;i++) {
        RAND_bytes((unsigned char *)array, arg);
//        MD5(array, arg, array);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    free(array);
    uint64_t t = as_nanoseconds(&end) - as_nanoseconds(&start);
    return t;
}

/**
 * chooseFunc == 0:使用stdlib定义的随机数生成函数
 * chooseFunc == 1:使用openssl定义的随机数生成函数
 * */
void fp_gen(uint64_t fp[N + 5][M + 5], int p, int chooseFunc) {
    int i = 0;
    while (i < M) {
        // cpu_affinity(1 % 8);
        int j = 0;
        while (j < N) {
            if(chooseFunc == 0) {
                long stallTime = stall_function((long) j * 50, p);
                fp[j][i] = stallTime;
            }else{
                long stallTime = stall_function_openssl((long) j * 50, p);
                fp[j][i] = stallTime;
            }
            j++;
        }
        i++;
    }
}

char* send_fp(string device_label, uint64_t fp[N + 5][M + 5]) {
    string res;
    // res += device_label + ":";
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            res += to_string(fp[i][j]);
            res += (j < M - 1) ? (",") : ("\n");
        }
    }
    int res_len = res.length();
    char* res_char = new char[res_len + 1];
    strcpy(res_char, res.c_str());
    // send_remote(res_char);
    // __android_log_print(ANDROID_LOG_ERROR, "hellohellotimetime----", "%s", res_char);
    return res_char;
}

void send_remote(char* res_char) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = inet_addr("192.168.1.107");
    serv_addr.sin_port = htons(5000);
    connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    int res_len = strlen(res_char);
    for (int i = 0; i < res_len; i += 1024) {
        send(sock, res_char + i, 1024, 0);
        // write(sock, res_char + i, 1024);
    }
    close(sock);
}
