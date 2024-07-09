#include "cpp_renderer.h"
#include <vector>
#include <malloc.h>
#include <android/log.h>
#include <cstring>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>

using namespace std;

// datas to be drawn
// no need to import whole glm for simple example
struct Vertex {
    float x, y;
};

const Vertex QUAD[4] = {
        {-0.0f, -0.0f},
        {0.7f, -0.0f},
        {-0.0f, 0.7f},
        {0.7f, 0.7f}
};


static const char VERTEX_SHADER[] =
        "#version 300 es\n"
        "  uniform int cur_stalled_vertex;\n"
        "    float stall_function(){\n"
        "        float res = 0.01;\n"
        "        for(int i = 1; i < 0x3ffff; i++){\n"
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
        "#version 300 es\n"
        "            precision mediump float;\n"
        "            out vec4 outColor;\n"
        "            \n"
        "            void main(void)\n"
        "            {\n"
        "                outColor = vec4(1,0,0,1);\n"
        "            }";

/** 用于传入IndexBuffer来绘制两个三角形从而组成矩形
 * 第一个三角形:0 1 2
 * 第二个三角形:3 2 1
*/
const unsigned int ORDER[6] = {0, 1, 2, 3, 2, 1};

// for shader loading
#define LOG_TAG "GLES C++"
#define ALOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)
#define ALOGV(...) __android_log_print(ANDROID_LOG_VERBOSE, LOG_TAG, __VA_ARGS__)


inline uint64_t as_nanoseconds(struct timespec* ts) {
    return ts->tv_sec * (uint64_t)1000000000L + ts->tv_nsec;
}

uint64_t cpp_renderer::measureVertex(GLint vertexIndex) {
    // Configure the stalled vertex index
    struct timespec start, end;
    int k = 4;

    /**
     * uniform变量是一种由cpu传到gpu的数据格式
     * 在opengl中，一旦着色器shader被创建，每个uniform都会获得一个id
     * glUniform函数实现了为uniform变量赋值，其中1代表只有1个变量，i代表整形
     * */
    glUniform1i(mVertexAttribPos, vertexIndex);
    glDrawArrays(GL_POINTS, 0, k);
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start);
    glFinish();//等待GPU完成绘图操作
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end);
    uint64_t stallTime = as_nanoseconds(&end) - as_nanoseconds(&start);

    // Assuming you have an appropriate definition for offscreenCan and convertToBlob
    // blob = offscreenCan.convertToBlob();

    return stallTime;
}



bool checkGlError(const char *funcName) {
    GLint err = glGetError();
    if(err != GL_NO_ERROR) {
        ALOGE("GL error after %s(): 0x%08x\n", funcName, err);
        return true;
    }
    return false;
}

GLuint  createShader(GLenum shaderType, const char* src) {
    GLuint shader = glCreateShader(shaderType);
    if(!shader) {
        checkGlError("glCreateShader");
        return 0;
    }
    glShaderSource(shader, 1, &src, NULL);

    GLint compiled = GL_FALSE;
    glCompileShader(shader);
    /** 错误检查开始 */
    glGetShaderiv(shader, GL_COMPILE_STATUS, &compiled);
    if(!compiled) {
        GLint infoLogLen = 0;
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &infoLogLen);
        if(infoLogLen > 0) {
            GLchar* infoLog = (GLchar*)malloc(infoLogLen);
            if(infoLog) {
                glGetShaderInfoLog(shader, infoLogLen, NULL, infoLog);
                ALOGE("Could not compile %s shader:\n%s\n",
                      shaderType == GL_VERTEX_SHADER ? "vertex" : "fragment",
                      infoLog);
                free(infoLog);
            }
        }
        glDeleteShader(shader);
        return 0;
    }
    /** 错误检查结束 */

    return shader;
}

GLuint createProgram(const char* vtxSrc, const char* fragSrc) {
    GLuint vtxShader = 0;
    GLuint fragShader = 0;
    GLuint program = 0;
    GLint linked = GL_FALSE;

    //vertex shader只对每个点渲染一次
    vtxShader = createShader(GL_VERTEX_SHADER, vtxSrc);
    if(!vtxShader)
        goto exit;

    //fragment shader对每个像素渲染一次
    fragShader = createShader(GL_FRAGMENT_SHADER, fragSrc);
    if(!fragShader)
        goto exit;

    program = glCreateProgram();
    if(!program) {
        checkGlError("glCreateProgram");
        goto exit;
    }
    glAttachShader(program, vtxShader);
    glAttachShader(program, fragShader);

    glLinkProgram(program);
    /**
     * glValidateProgram(program);这行代码是自己加的，原本没有
     * */
    glValidateProgram(program);
    glGetProgramiv(program, GL_LINK_STATUS, &linked);
    if(!linked) {
        ALOGE("Could not link program");
        GLint infoLogLen = 0;
        glGetProgramiv(program, GL_INFO_LOG_LENGTH, &infoLogLen);
        if(infoLogLen) {
            GLchar* infoLog = (GLchar*)malloc(infoLogLen);
            if(infoLog) {
                glGetProgramInfoLog(program, infoLogLen, NULL, infoLog);
                // ALOGE("Could not link program:\n%s\n", infoLog);
                printf("Could not link program");
                free(infoLog);
            }
        }
        glDeleteProgram(program);
        program = 0;
    }

    exit:
    glDeleteShader(vtxShader);
    glDeleteShader(fragShader);
    return program;
}

// renderer
void cpp_renderer::draw() {
    string res;
    int k = 4;
    glUseProgram(mProgram);

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    /** glBindBuffer 绑定缓冲区 */
    glBindBuffer(GL_ARRAY_BUFFER, mVertexBuffer);
    glEnableVertexAttribArray(0);
    /** glVertexAttribPointer会告诉openGL缓存的布局 */
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, (const GLvoid*)0);


    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mIndexBuffer);
    // glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, (void*)0);

    // 测试时间开始
    for(int i=0 ; i<(1 << k); i++){
        res += to_string(measureVertex(i));
        res += (i < (1 << k) - 1) ? (",") : ("\n");
    }
    int res_len = res.length();
    char* res_char = new char[res_len + 1];
    strcpy(res_char, res.c_str());
    __android_log_print(ANDROID_LOG_ERROR, "hellohellotimetime----", "%s", res_char);
    // 测试时间结束

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
    glDisableVertexAttribArray(0);
}

void cpp_renderer::init() {
    /**
     * glGenBuffers创建缓冲区，第一个参数为缓冲区数量，第二个参数会将缓冲区id返回
     * 如glGenBuffers(1, &mVertexBuffer);创建1个缓冲区，将缓冲区id赋值给mVertexBuffer
     * */
    glGenBuffers(1, &mVertexBuffer);
    glBindBuffer(GL_ARRAY_BUFFER, mVertexBuffer);
    std::vector<Vertex> testVertices(QUAD, QUAD + 4);
    /** 给缓冲区指定数据有两种方式，一是指定它的大小并给他数据，二是仅仅用数据来更新他
     * glBufferData:给缓冲区指定数据
     * 参数一指定缓冲区类型，参数二指定缓冲区大小
     * */
    glBufferData(GL_ARRAY_BUFFER, sizeof(Vertex) * testVertices.size(), &testVertices[0], GL_STATIC_DRAW);
    glBindBuffer(GL_ARRAY_BUFFER, 0);

    /** 索引缓冲区允许重用已有的顶点 */
    glGenBuffers(1, &mIndexBuffer);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mIndexBuffer);

    std::vector<unsigned int> testOrder(ORDER, ORDER + 6);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(unsigned)*testOrder.size(), &testOrder[0], GL_STATIC_DRAW);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);

    mProgram = createProgram(VERTEX_SHADER, FRAGMENT_SHADER);
    /** mVertexAttribPos类型为unsigned int，表示下标 */
    mVertexAttribPos = glGetUniformLocation(mProgram, "cur_stalled_vertex");
}

