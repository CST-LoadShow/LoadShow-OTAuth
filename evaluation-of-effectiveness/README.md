# LoadShow for Android

## Usage
You could download the .apk file in our release version or follow these three steps to compile with codes yourself.
1. Install CMake and NDK in Android Studio
2. Compile the code in Android Studio
3. Run the application on your mobile phone or Android Simulator

## Project Content
The key codes are located in the `android_fingerprint_extraction/app/src/main` directory
|Directory|Description|
|:---:|:---:|
|cpp|Native C code, responsible for the specific implementation of fingerprint extraction|
|java|Extract management and set configuration|
|res|Interface and graphic resource files|

## Parameter `p` in Fingerprinting
The following two loops are the most important pieces of code for fingerprinting, and the parameter `p` is the key to controlling the time and effect of fingerprinting.

CPU fingerprinting code:

(android_fingerprint_extraction/app/src/main/cpp/native-lib.cpp)
```c
uint64_t stall_function_openssl(long arg, int p){
    struct timespec start, end;
    time_t time1 = (long)10;
    srand(time(&time1));
    int len = arg * sizeof(unsigned char);
    unsigned char* array = (unsigned char*)malloc(len);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    for(int i = 0;i<p;i++) {
        RAND_bytes((unsigned char *)array, arg);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    free(array);
    uint64_t t = as_nanoseconds(&end) - as_nanoseconds(&start);
    return t;
}
```

GPU fingerprinting code:

(android_fingerprint_extraction/app/src/main/cpp/cpp_offscreen_gpu.cpp)
```c
uint64_t measureVertex(GLuint program, GLint vertexIndex) {
    struct timespec start, end;
    GLsync syncObject = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);
    glUniform1i(aPositionLocation, vertexIndex);

    glDrawArrays(GL_POINTS, 0, k);

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    glClientWaitSync(syncObject, 0, GL_TIMEOUT_IGNORED);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    eglSwapBuffers(eglDisp, eglSurface);

    uint64_t stallTime = as_nanoseconds(&end) - as_nanoseconds(&start);
    glDeleteSync(syncObject);
    return stallTime;
}
```
