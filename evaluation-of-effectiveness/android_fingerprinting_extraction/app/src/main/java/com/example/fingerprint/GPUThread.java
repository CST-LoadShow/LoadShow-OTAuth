package com.example.fingerprint;


import android.os.Handler;
import android.os.Message;
import android.widget.Button;

import java.text.SimpleDateFormat;
import java.util.Date;

public class GPUThread extends Thread{
    public volatile boolean isRunning = false;
    public static RemoteServer remoteServer = null;
    private static final int COMPLETED = 0;
    public int count = 0;
    public Button button;
    public boolean continueFlag = false;
    public int waitTime;
    public int maxCount;

    public GPUThread(Button button){
        this.button = button;
        this.waitTime = NativeLib.waitTime;
        this.maxCount = NativeLib.gpuCount;
        setName("GPU_fingerprint_thread");
    }

    private Handler handler = new Handler(){
        @Override
        public void handleMessage(Message msg) {
            if (msg.what == COMPLETED) {
                 button.setText("GPU test start"); //UI更改操作
            }

        }
    };


    @Override
    public void run(){
        if(remoteServer == null){
            remoteServer = new RemoteServer();
        }

        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String cur_time = dateFormat.format(new Date());

        long startWait = System.currentTimeMillis();
        while(isRunning){
//            long wait0 = System.currentTimeMillis();
            NativeLib.init();
//            long wait1 = System.currentTimeMillis();
            String gpuTimeResult = NativeLib.draw();
//            long wait2 = System.currentTimeMillis();
            NativeLib.release();
//            long wait3 = System.currentTimeMillis();
            long endWait = System.currentTimeMillis();
            if(endWait - startWait > waitTime) {
                remoteServer.postString(gpuTimeResult, "81.70.33.32","8184", "/get_offscreen_traces", cur_time);
//                System.out.println("count:" + count + "\t" + gpuTimeResult);
//                System.out.println("init time:\t" + (wait1 - wait0));
//                System.out.println("draw time:\t" + (wait2 - wait1));
//                System.out.println("release time:\t" + (wait3 - wait2));
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
