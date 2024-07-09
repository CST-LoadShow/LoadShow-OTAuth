package com.example.fingerprint.service;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.os.IBinder;
import android.util.Log;
import android.widget.Button;

import com.example.fingerprint.CPUThread;
import com.example.fingerprint.GPUThread;

/** 第二个Service */
public class MyService extends Service {
    public CPUThread cpuThread = null;
    public GPUThread gpuThread = null;
    public Button button = null;

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    // onCreate()方法会在服务创建的时候调用
    @Override
    public void onCreate() {
        super.onCreate();
        Log.d("MyService", "onCreate executed");
    }

    // onStartCommand()方法会在每次服务启动的时候调用
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d("MyService", "onStartCommand executed");
        int return_int = super.onStartCommand(intent, flags, startId);
//        cpuThread = new CPUThread(button);
//        cpuThread.isRunning = true;
//        cpuThread.start();

        gpuThread = new GPUThread(button);
        gpuThread.isRunning = true;
        gpuThread.start();
        return return_int;
    }

    // onDestroy()方法会在服务销毁的时候 调用
    @Override
    public void onDestroy() {
        // cpuThread.isRunning = false;
        super.onDestroy();
        Log.d("MyService", "onDestroy executed");
    }
}