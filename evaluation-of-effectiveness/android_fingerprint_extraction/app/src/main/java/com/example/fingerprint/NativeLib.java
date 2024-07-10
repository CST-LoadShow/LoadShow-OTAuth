package com.example.fingerprint;

public class NativeLib {

    public static String CPU_IP = "";
    public static String CPU_PORT = "";
    public static String GPU_IP = "";
    public static String GPU_PORT = "";

    /** 等待时间 */
    public static int waitTime = 20000;
    /** CPU测试数量 */
    public static int cpuCount = 32;
    /** GPU测试数量 */
    public static int gpuCount = 64*32;
    /** 目标app名 */
    public static String targetAppName = "";
    /** 选用Service类型 */
    public static String serviceAppName = "Thread";
    /**
    * 可选："", "_glFinish", "_eglSwapBuffers"
    * */
    public static String GPU_FUNCTION = "";

    static {
        System.loadLibrary("fingerprint");
        System.loadLibrary("offscreen_gpu");
    }
    /**
     * A native method that is implemented by the 'openssl_test' native library,
     * which is packaged with this application.
     */
    public static native String getTimeFromJNI();
    public static native String getTimeFromOpenGL();

    public static native void init();
    public static native String draw();
    public static native void release();
    public static boolean isRunning = false;

}
