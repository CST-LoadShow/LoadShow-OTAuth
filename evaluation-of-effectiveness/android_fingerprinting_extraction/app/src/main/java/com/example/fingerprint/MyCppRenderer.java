package com.example.fingerprint;

public class MyCppRenderer {
    static {
        System.loadLibrary("cpp_renderer");
    }
    void draw() {
        _draw();
    }

    void init() {
        _init();
    }

    private native void _init();
    private native void _draw();
    // Used to load the 'cpp_renderer' library on application startup.

}


