#ifndef OPENCVNDK_CPP_RENDERER_H
#define OPENCVNDK_CPP_RENDERER_H

#include <GLES2/gl2.h>

class cpp_renderer {
public:
    // Initialize shaders and GL buffers
    void init();

    // Render the OpenGL buffers using the shader
    void draw();

    uint64_t measureVertex(GLint vertexIndex);

private:
    GLuint mVertexBuffer;
    GLuint mIndexBuffer;

    GLuint mProgram;
    GLint mVertexAttribPos;

    GLuint mOffscreenFramebuffer;
    GLuint mOffscreenTexture;

    unsigned int mElementCount = 0;
};

#endif //OPENCVNDK_CPP_RENDERER_H

