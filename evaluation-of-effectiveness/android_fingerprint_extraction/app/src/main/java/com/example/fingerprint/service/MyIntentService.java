package com.example.fingerprint.service;

import android.app.IntentService;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;
import android.widget.Button;

import androidx.annotation.Nullable;

import com.example.fingerprint.NativeLib;
import com.example.fingerprint.RemoteServer;


/** 第一个Service */
public class MyIntentService extends IntentService {
    public int count = 0;
    public Button button = null;
    private static final int COMPLETED = 0;
    public int waitTime;
    public int maxCount;
    public static RemoteServer remoteServer = null;

    /**
     * @param name
     * @deprecated
     */
    public MyIntentService(String name) {
        super(name);
    }

    public MyIntentService() {
        super("MyService");

    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    protected void onHandleIntent(@Nullable Intent intent) {
        if(remoteServer == null){
            remoteServer = new RemoteServer();
        }
        count = 0;
        long startWait = System.currentTimeMillis();
        while(NativeLib.isRunning){
            String cpuTimeResult = NativeLib.getTimeFromJNI();
            long endWait = System.currentTimeMillis();
            // 点击按钮后20s向服务器发送数据
            if(endWait - startWait > waitTime) {
                remoteServer.postString(cpuTimeResult, "81.70.33.32","8084", "/get_fingerprint", null);
                // System.out.println(cpuTimeResult);
                count += 1;
                if (count >= maxCount) {
                    NativeLib.isRunning = false;
                    System.out.println("============================== Running Finish ==============================");
                    break;
                }
            }
        }
    }

    // onCreate()方法会在服务创建的时候调用
    @Override
    public void onCreate() {
        super.onCreate();
        waitTime = 20000;
        maxCount = 32;
        Log.d("MyIntentService", "onCreate executed");
    }


    // onDestroy()方法会在服务销毁的时候 调用
    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d("MyIntentService", "onDestroy executed");
    }
}


