#include <jni.h>
#include <memory>
#include "cpp_renderer.h"

std::unique_ptr<cpp_renderer> mRenderer;

extern "C" {
JNIEXPORT void JNICALL
Java_com_example_fingerprint_Natilib__1init(JNIEnv *env, jobject instance) {
mRenderer->init();
}

JNIEXPORT void JNICALL
Java_com_example_fingerprint_Natilib__1draw(JNIEnv * env, jobject instance) {
mRenderer->draw();
}


JNIEXPORT void JNICALL
Java_com_example_fingerprint_MyCppRenderer__1init(JNIEnv *env, jobject instance) {
    mRenderer->init();
}

JNIEXPORT void JNICALL
Java_com_example_fingerprint_MyCppRenderer__1draw(JNIEnv * env, jobject instance) {
    mRenderer->draw();
}

// Create renderer instance
jint JNI_OnLoad(JavaVM* vm, void* reserved) {
    mRenderer = std::unique_ptr<cpp_renderer> {new cpp_renderer{}};

    JNIEnv* env;
    if(vm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6) != JNI_OK) {
        return -1;
    }
    return JNI_VERSION_1_6;
}
}
