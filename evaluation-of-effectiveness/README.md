# LoadShow for Android

## Usage
You could download the .apk file in our release version or follow these three steps to compile the codes yourself.
1. Install `CMake` and `NDK` in Android Studio. 
2. Compile the code in Android Studio. 
3. Run the application on your mobile phone or Android Simulator. 

## Project Content
The key codes are located in the `android_fingerprint_extraction/app/src/main` directory. 
|Directory|Description|
|:---:|:---|
|cpp|Native C code, responsible for the specific implementation of fingerprint extraction|
|java|Extract management and set configuration|
|res|Interface and graphic resource files|

## Parameter `p` in Fingerprinting
The following functions are the most important pieces of code for fingerprinting, and the parameter `p` is the key to controlling the time and effect of fingerprinting.

#### CPU fingerprinting code:

The code are located in the `android_fingerprint_extraction/app/src/main/cpp/native-lib.cpp` file.

- In the following code, the `RAND_bytes` function from OpenSSL is used as a delay function, and the `clock_gettime` function is utilized for timing, achieving nanosecond-level timing precision.

```c
uint64_t stall_function_openssl(long arg, int p)
{
    struct timespec start, end;
    time_t time1 = (long)10;
    srand(time(&time1));
    int len = arg * sizeof(unsigned char);
    unsigned char* array = (unsigned char*)malloc(len);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    for(int i = 0; i < CPU_P; i++)
    {
        RAND_bytes((unsigned char *)array, arg);
    }
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    free(array);
    uint64_t t = as_nanoseconds(&end) - as_nanoseconds(&start);
    return t;
}
```

#### GPU fingerprinting code:

The code are located in the `android_fingerprint_extraction/app/src/main/cpp/cpp_offscreen_gpu.cpp` file.

- `stall_function` is set in the VERTEX_SHADER as a delay function.

```javascript
float stall_function()
{
    float res = 0.01;
    for(int i = 1; i < GPU_P; i++)
    {
        res = sinh(res);
    }
    return res;
}
```

- When extracting application fingerprints, the `draw` function loads the aforementioned VERTEX_SHADER and selects different vertices to execute the shader.

```c
extern "C" JNIEXPORT jstring JNICALL draw
        (JNIEnv*env, jclass clazz)
{
    string result;
    GLuint program = prepare();
    glUseProgram(program);
    glVertexAttribPointer(0,2,GL_FLOAT,GL_FALSE,0,tableVerticesWithTriangles);
    glEnableVertexAttribArray(0);
    //draw something
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    for(int i=0 ; i<(1 << k); i++){
        result += to_string(measureVertex(program, i));
        result += (i < (1 << k) - 1) ? (",") : ("\n");
    }
    int res_len = result.length();
    char* res_char = new char[res_len + 1];
    strcpy(res_char, result.c_str());
    return env->NewStringUTF(res_char);
}
```

- Build a synchronization object and record the execution time of the synchronization function `glClientWaitSync` as part of the GPU fingerprint application every time a drawing instruction is issued to the GPU.

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

## Settings of `p`

| Settings | `CPU_P` | `GPU_P` |
| :------  | :-----------: | :-----------: |
| Android | `500` | `0xffff` |
