package com.example.fingerprint.service;

import android.app.Notification;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.graphics.BitmapFactory;
import android.os.IBinder;
import android.util.Log;
import android.widget.Button;

import androidx.core.app.NotificationCompat;

import com.example.fingerprint.CPUThread;
import com.example.fingerprint.MainActivity;
import com.example.fingerprint.R;

public class MyForegroundService extends Service {
    public CPUThread cpuThread = null;
    public Button button = null;

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    // onCreate()方法会在服务创建的时候调用
    @Override
    public void onCreate() {
        super.onCreate();
        //在service的onCreate（）方法里加入如下代码，则可以将一个服务提升为前台服务

        Intent intent = new Intent(this, MainActivity.class);
        PendingIntent pi = PendingIntent.getActivity(this, 0, intent, 0);

        Notification notification = new NotificationCompat.Builder(this)
                .setContentTitle("This is content title")
                .setContentText("This is content text")
                .setWhen(System.currentTimeMillis())
                .setSmallIcon(R.mipmap.fingerprint_icon)
                .setLargeIcon(BitmapFactory.decodeResource(getResources(), R.mipmap.fingerprint_icon))
                .setContentIntent(pi)
                .build();

        // 调用 startForeground()方法后就会让 MyService 变成一个前台服务，并在系统状态栏显示出来
        // 注意：startForeground()第一个参数必须大于0，否则无法在通知栏显示
        startForeground(1, notification);
        Log.d("MyService", "onCreate executed");
    }

    // onStartCommand()方法会在每次服务启动的时候调用
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d("MyService", "onStartCommand executed");
        int return_int = super.onStartCommand(intent, flags, startId);
        cpuThread = new CPUThread(button);
        cpuThread.isRunning = true;
        cpuThread.start();
        return return_int;
    }

    // onDestroy()方法会在服务销毁的时候 调用
    @Override
    public void onDestroy() {
        cpuThread.isRunning = false;
        super.onDestroy();
        Log.d("MyService", "onDestroy executed");
    }
}
