//
// Created by guoyuxiao on 2024/3/4.
//

#include <jni.h>
#include <iostream>
#include <stdlib.h>
#include <EGL/egl.h>
#include <EGL/eglext.h>
#include <GLES3/gl3.h>
#include <GLES3/gl3ext.h>
#include <android/log.h>
#include <vector>
#include <malloc.h>
#include <cstring>
#include <GLES2/gl2ext.h>



#define  LOG_TAG    "offscreen"
#define  LOGI(...)  __android_log_print(ANDROID_LOG_INFO,LOG_TAG,__VA_ARGS__)


using namespace std;


static EGLConfig eglConf;
static EGLSurface eglSurface;
static EGLContext eglCtx;
static EGLDisplay eglDisp;
static GLuint aPositionLocation;
static GLuint program;
inline uint64_t as_nanoseconds(struct timespec* ts);
GLuint prepare();
int k = 4;

static const char VERTEX_SHADER[] =
    "#version 300 es\n"
    "  uniform int cur_stalled_vertex;\n"
    "    float stall_function(){\n"
    "        float res = 0.01;\n"
    "        for(int i = 1; i < 0xffff; i++){\n"
    "            res = sinh(res);\n"
    "        }\n"
    "        return res;\n"
    "    }\n"
    "    void main(void){\n"
    "      if ((cur_stalled_vertex & (1 << gl_VertexID)) != 0) {\n"
    "      //if (cur_stalled_vertex == gl_VertexID) {\n"
    "        gl_Position = vec4(stall_function(),0, 1,1);\n"
    "      } else {\n"
    "        gl_Position = vec4(0,0, 1,1);\n"
    "      }\n"
    "        gl_PointSize = 1.0; \n"
    "    }";

static const char FRAGMENT_SHADER[] =
    "   #version 300 es\n"
    "   precision mediump float;\n"
    "   out vec4 outColor;\n"
    "   \n"
    "   void main(void)\n"
    "   {\n"
    "       outColor = vec4(1,0,0,1);\n"
    "   }";


const float tableVerticesWithTriangles[] = {
    -0.5f,-0.5f,
    0.5f, 0.5f,
    -0.5f, 0.5f,
    0.5f,-0.5f,
};

inline uint64_t as_nanoseconds(struct timespec* ts) {
    return ts->tv_sec * (uint64_t)1000000000L + ts->tv_nsec;
}


extern "C" JNIEXPORT void JNICALL Java_com_example_fingerprint_NativeLib_init
(JNIEnv*env, jclass clazz)
{
    // EGL config attributes
    const EGLint confAttr[] =
        {
            EGL_RENDERABLE_TYPE, EGL_OPENGL_ES2_BIT,// very important!
            EGL_SURFACE_TYPE,EGL_PBUFFER_BIT,//EGL_WINDOW_BIT EGL_PBUFFER_BIT we will create a pixelbuffer surface
            EGL_RED_SIZE,   8,
            EGL_GREEN_SIZE, 8,
            EGL_BLUE_SIZE,  8,
//            EGL_ALPHA_SIZE, 8,// if you need the alpha channel
//            EGL_DEPTH_SIZE, 8,// if you need the depth buffer
            EGL_STENCIL_SIZE,8,
            EGL_NONE
        };
    // EGL context attributes
    const EGLint ctxAttr[] = {
        EGL_CONTEXT_CLIENT_VERSION, 2,// very important!
        EGL_NONE
    };
    // surface attributes
    // the surface size is set to the input frame size
    const EGLint surfaceAttr[] = {
        EGL_WIDTH,512,
        EGL_HEIGHT,512,
        EGL_NONE
    };
    EGLint eglMajVers, eglMinVers;
    EGLint numConfigs;

    eglDisp = eglGetDisplay(EGL_DEFAULT_DISPLAY);
    if(eglDisp == EGL_NO_DISPLAY)
    {
        //Unable to open connection to local windowing system
        LOGI("Unable to open connection to local windowing system");
    }
    if(!eglInitialize(eglDisp, &eglMajVers, &eglMinVers))
    {
        // Unable to initialize EGL. Handle and recover
        LOGI("Unable to initialize EGL");
    }
    // LOGI("EGL init with version %d.%d", eglMajVers, eglMinVers);
    // choose the first config, i.e. best config
    if(!eglChooseConfig(eglDisp, confAttr, &eglConf, 1, &numConfigs))
    {
        LOGI("some config is wrong");
    }
    else
    {
        // LOGI("all configs is OK");
    }
    // create a pixelbuffer surface
    eglSurface = eglCreatePbufferSurface(eglDisp, eglConf, surfaceAttr);
    if(eglSurface == EGL_NO_SURFACE)
    {
        switch(eglGetError())
        {
            case EGL_BAD_ALLOC:
            // Not enough resources available. Handle and recover
            LOGI("Not enough resources available");
            break;
            case EGL_BAD_CONFIG:
            // Verify that provided EGLConfig is valid
            LOGI("provided EGLConfig is invalid");
            break;
            case EGL_BAD_PARAMETER:
            // Verify that the EGL_WIDTH and EGL_HEIGHT are
            // non-negative values
            LOGI("provided EGL_WIDTH and EGL_HEIGHT is invalid");
            break;
            case EGL_BAD_MATCH:
            // Check window and EGLConfig attributes to determine
            // compatibility and pbuffer-texture parameters
            LOGI("Check window and EGLConfig attributes");
            break;
        }
    }
    eglCtx = eglCreateContext(eglDisp, eglConf, EGL_NO_CONTEXT, ctxAttr);
    if(eglCtx == EGL_NO_CONTEXT)
    {
        EGLint error = eglGetError();
        if(error == EGL_BAD_CONFIG)
        {
            // Handle error and recover
            LOGI("EGL_BAD_CONFIG");
        }
    }
    if(!eglMakeCurrent(eglDisp, eglSurface, eglSurface, eglCtx))
    {
        LOGI("MakeCurrent failed");
    }
    // LOGI("initialize success!");

    prepare();
}

GLuint prepare()
{
//    const char*vertex_shader=VERTEX_SHADER;
//    const char*fragment_shader=FRAGMENT_SHADER;
    const char*vertex_shader=VERTEX_SHADER;
    const char*fragment_shader=FRAGMENT_SHADER;
    glPixelStorei(GL_UNPACK_ALIGNMENT,1);
    glClearColor(0.0,0.0,0.0,0.0);
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);
    glCullFace(GL_BACK);
    glViewport(0,0,512,512);
    GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
    glShaderSource(vertexShader,1,&vertex_shader,NULL);
    glCompileShader(vertexShader);
    GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(fragmentShader,1,&fragment_shader,NULL);
    glCompileShader(fragmentShader);
    program = glCreateProgram();
    glAttachShader(program, vertexShader);
    glAttachShader(program, fragmentShader);
    glLinkProgram(program);
    aPositionLocation = glGetUniformLocation(program, "cur_stalled_vertex");
    return program;
}

#define SELECT_GPU_METHOD 10

uint64_t measureVertex(GLuint program, GLint vertexIndex) {
    struct timespec start, end;
    /**
     * uniform变量是一种由cpu传到gpu的数据格式
     * 在opengl中，一旦着色器shader被创建，每个uniform都会获得一个id
     * glUniform函数实现了为uniform变量赋值，其中1代表只有1个变量，i代表整形
     * */

#if SELECT_GPU_METHOD == 10
    /** ============================ CPU端计时 原始方法 ================================== **/
    GLsync syncObject = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);
    glUniform1i(aPositionLocation, vertexIndex);

    glDrawArrays(GL_POINTS, 0, k);

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    glClientWaitSync(syncObject, 0, GL_TIMEOUT_IGNORED);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    eglSwapBuffers(eglDisp, eglSurface);

    uint64_t stallTime = as_nanoseconds(&end) - as_nanoseconds(&start);
    glDeleteSync(syncObject);

#elif SELECT_GPU_METHOD == 11
    /** ============================ CPU端计时 变种1 (test3)================================== **/

    glUniform1i(aPositionLocation, vertexIndex);

    glDrawArrays(GL_POINTS, 0, k);
    GLsync syncObject = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    glClientWaitSync(syncObject, 0, GL_TIMEOUT_IGNORED);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    eglSwapBuffers(eglDisp, eglSurface);

    uint64_t stallTime = as_nanoseconds(&end) - as_nanoseconds(&start);
    glDeleteSync(syncObject);

#elif SELECT_GPU_METHOD == 20
    /** ============================ CPU端计时 test1方法 ================================== **/

    glUniform1i(aPositionLocation, vertexIndex);

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    // test1
    glDrawArrays(GL_POINTS, 0, k);
    /* 同步对象置于glDrawArrays之后 */   // test2
    GLsync syncObject = glFenceSync(GL_SYNC_GPU_COMMANDS_COMPLETE, 0);
    // test3
    // glFinish();//等待GPU完成绘图操作
    glClientWaitSync(syncObject, 0, GL_TIMEOUT_IGNORED);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
//    eglSwapBuffers(eglDisp, eglSurface);

    uint64_t stallTime = as_nanoseconds(&end) - as_nanoseconds(&start);
    glDeleteSync(syncObject);

#elif SELECT_GPU_METHOD == 30
    /** ============================ GPU端计时 ================================== **/
    // 检查并启用扩展
    if (!eglGetProcAddress("glGenQueriesEXT") ||
        !eglGetProcAddress("glBeginQueryEXT") ||
        !eglGetProcAddress("glEndQueryEXT") ||
        !eglGetProcAddress("glGetQueryObjectuivEXT")) {
        fprintf(stderr, "EXT_disjoint_timer_query not supported\n");
        return -1;
    }

// 获取扩展函数指针
//    PFNGLGENQUERIESEXTPROC glGenQueriesEXT = (PFNGLGENQUERIESEXTPROC)eglGetProcAddress("glGenQueriesEXT");
//    PFNGLBEGINQUERYEXTPROC glBeginQueryEXT = (PFNGLBEGINQUERYEXTPROC)eglGetProcAddress("glBeginQueryEXT");
//    PFNGLENDQUERYEXTPROC glEndQueryEXT = (PFNGLENDQUERYEXTPROC)eglGetProcAddress("glEndQueryEXT");
    PFNGLGETQUERYOBJECTUIVEXTPROC glGetQueryObjectuivEXT = (PFNGLGETQUERYOBJECTUIVEXTPROC)eglGetProcAddress("glGetQueryObjectuivEXT");


    glUniform1i(aPositionLocation, vertexIndex);
    GLuint query;
    glGenQueries(1, &query);


    /** glGenQueries，glBeginQuery，glEndQuery **/
    // 开始GPU计时
    glBeginQuery(GL_TIME_ELAPSED_EXT, query);
    glDrawArrays(GL_POINTS, 0, k);
    glEndQuery(GL_TIME_ELAPSED_EXT);
    // 查询结果是否可用
    GLuint available = 0;
    while(!available)
    {
        glGetQueryObjectuivEXT(query, GL_QUERY_RESULT_AVAILABLE_EXT, &available);
    }
    // 获取查询结果
    GLuint stallTime = 0;
    glGetQueryObjectuivEXT(query, GL_QUERY_RESULT_EXT, &stallTime);
    // Clean up
    glDeleteQueries(1, &query);
#else
    uint64_t stallTime = 0;
#endif

    return stallTime;
}


extern "C" JNIEXPORT jstring JNICALL Java_com_example_fingerprint_NativeLib_draw
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
        /** 原始代码 */
         result += to_string(measureVertex(program, i));
        /** 测试开始 */
//        struct timespec sstart, eend;
//        clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &sstart);
//        measureVertex(program, i);
//        clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &eend);
//        uint64_t sstallTime = as_nanoseconds(&eend) - as_nanoseconds(&sstart);
//        result += to_string(sstallTime);
        /** 测试结束 */

        result += (i < (1 << k) - 1) ? (",") : ("\n");
    }
    int res_len = result.length();
    char* res_char = new char[res_len + 1];
    strcpy(res_char, result.c_str());
    return env->NewStringUTF(res_char);
}

extern "C" JNIEXPORT void JNICALL Java_com_example_fingerprint_NativeLib_release
(JNIEnv*env, jclass clazz)
{
    eglMakeCurrent(eglDisp, EGL_NO_SURFACE, EGL_NO_SURFACE, EGL_NO_CONTEXT);
    eglDestroyContext(eglDisp, eglCtx);
    eglDestroySurface(eglDisp, eglSurface);
    eglTerminate(eglDisp);

    eglDisp = EGL_NO_DISPLAY;
    eglSurface = EGL_NO_SURFACE;
    eglCtx = EGL_NO_CONTEXT;
}






