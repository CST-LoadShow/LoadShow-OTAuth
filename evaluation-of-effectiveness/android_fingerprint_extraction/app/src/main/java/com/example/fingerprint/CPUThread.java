package com.example.fingerprint;

import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.Message;
import android.widget.Button;

import com.example.fingerprint.service.MyForegroundService;


public class CPUThread extends Thread{
    public volatile boolean isRunning = true;
    public static RemoteServer remoteServer = null;
    public int count = 0;
    public Button button = null;
    private static final int COMPLETED = 0;
    public int waitTime;
    public int maxCount;

    public CPUThread(Button button){
        this.button = button;
        this.waitTime = NativeLib.waitTime;
        this.maxCount = NativeLib.cpuCount;
        setName("CPU_fingerprint_thread");
    }

    private Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            if (msg.what == COMPLETED) {
                 button.setText("CPU test start"); //UI更改操作
            }
        }
    };

    @Override
    public void run(){
        if(remoteServer == null){
            remoteServer = new RemoteServer();
        }
        count = 0;
        long startWait = System.currentTimeMillis();
        while(isRunning){
            String cpuTimeResult = NativeLib.getTimeFromJNI();
            long endWait = System.currentTimeMillis();
            // 点击按钮后20s向服务器发送数据
            if(endWait - startWait > waitTime) {
                remoteServer.postString(cpuTimeResult, "81.70.33.32","8084", "/get_fingerprint", null);
                // System.out.println(cpuTimeResult);
                count += 1;
                if (count >= maxCount) {
                    isRunning = false;
                    System.out.println("============================== Running Finish ==============================");
                    Message message = new Message();
                    message.what = COMPLETED;
                    handler.sendMessage(message);
                    break;
                }
            }
        }

    }

}
