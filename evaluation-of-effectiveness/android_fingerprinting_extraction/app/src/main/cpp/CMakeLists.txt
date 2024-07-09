# For more information about using CMake with Android Studio, read the
# documentation: https://d.android.com/studio/projects/add-native-code.html

# Sets the minimum version of CMake required to build the native library.

cmake_minimum_required(VERSION 3.18.1)

# *****
set(CMAKE_VERBOSE_MAKEFILE on)
include_directories(include)

# =====  OPENGL  =====
set(OPENGL_LIB GLESv2)
set(OPENGL_LIB_v3 GLESv3)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=gnu++11 -fexceptions -frtti")
# *****


# Declares and names the project.

project("fingerprint")


# Creates and names a library, sets it as either STATIC
# or SHARED, and provides the relative paths to its source code.
# You can define multiple libraries, and CMake builds them for you.
# Gradle automatically packages shared libraries with your APK.

add_library( # Sets the name of the library.
        fingerprint

        # Sets the library as a shared library.
        SHARED

        # Provides a relative path to your source file(s).
        native-lib.cpp)

add_library(
        offscreen_gpu
        SHARED
        cpp_offscreen_gpu.cpp
)

# *****
add_library( # Sets the name of the library.
        cpp_renderer

        # Sets the library as a shared library.
        SHARED

        # Provides a relative path to your source file(s).
        cpp_renderer_interface.cpp
        cpp_renderer.cpp)
# *****


# Specifies libraries CMake should link to your target library. You
# can link multiple libraries, such as libraries you define in this
# build script, prebuilt third-party libraries, or system libraries.


include_directories(
#        ${CMAKE_CURRENT_SOURCE_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/include
#        ${CMAKE_CURRENT_SOURCE_DIR}/include/openssl
)


add_library(# Sets the name of the library.
        openssl-crypto
        # Sets the library as a static library.
        STATIC
        IMPORTED)

set_target_properties(
        # Specifies the target library.
        openssl-crypto
        # Specifies the parameter you want to define.
        PROPERTIES IMPORTED_LOCATION
        # Provides the path to the library you want to import.
        ${CMAKE_CURRENT_SOURCE_DIR}/libs/${ANDROID_ABI}/libcrypto.a)

add_library(# Sets the name of the library.
        openssl-ssl
        # Sets the library as a static library.
        STATIC
        IMPORTED)

set_target_properties(
        # Specifies the target library.
        openssl-ssl
        # Specifies the parameter you want to define.
        PROPERTIES IMPORTED_LOCATION
        # Provides the path to the library you want to import.
        ${CMAKE_CURRENT_SOURCE_DIR}/libs/${ANDROID_ABI}/libssl.a)


# *****
target_link_libraries( # Specifies the target library.
        cpp_renderer
        -lEGL
        -llog
        # Links the target library to the log library
        # included in the NDK.
        # ===========
        ${OPENGL_LIB}
        ${OPENGL_LIB_v3}
        # ===========
        ${log-lib} )
# *****


target_link_libraries(
        offscreen_gpu
        -lEGL
        -llog
        ${OPENGL_LIB}
        ${OPENGL_LIB_v3}
        ${log-lib} )


        # Searches for a specified prebuilt library and stores the path as a
# variable. Because CMake includes system libraries in the search path by
# default, you only need to specify the name of the public NDK library
# you want to add. CMake verifies that the library exists before
# completing its build.

find_library( # Sets the name of the path variable.
        log-lib

        # Specifies the name of the NDK library that
        # you want CMake to locate.
        log)

target_link_libraries( # Specifies the target library.
        fingerprint

        # Links the target library to the log library
        # included in the NDK.
        PUBLIC
        openssl-crypto
        openssl-ssl
        ${log-lib} )

target_link_libraries( # Specifies the target library.
        fingerprint

        # Links the target library to the log library
        # included in the NDK.
        PUBLIC
        openssl-ssl
        ${log-lib} )