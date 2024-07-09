package com.example.fingerprint;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.Intent;
import android.content.pm.ConfigurationInfo;

import android.os.Build;
import android.os.Bundle;

import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.example.fingerprint.databinding.ActivityMainBinding;
import com.example.fingerprint.service.MyForegroundService;


public class MainActivity extends Activity {
    // AppCompatActivity
    // Used to load the 'openssl_test' library on application startup.

    private ActivityMainBinding binding;
    public Button cpu_button = null;
    public Button gpu_button = null;
    public GPUButtonCall gpu_btn_call;
    public EditText targetAppName = null;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        NativeLib.release();

        targetAppName = (EditText) findViewById(R.id.targetAppName);

        cpu_button = (Button)findViewById(R.id.cpu_btn);
        cpu_button.setOnClickListener(new CPUButtonCall(this, cpu_button, targetAppName));

        gpu_button = (Button)findViewById(R.id.gpu_btn);
        gpu_btn_call = new GPUButtonCall(this, gpu_button, targetAppName);
        // gpu_btn_call.gpuThread.isRunning = false;
        gpu_button.setOnClickListener(gpu_btn_call);
        // myGLSurfaceView = new MyGLSurfaceView(this);
        // 替换界面
        // setContentView(myGLSurfaceView);

        // Example of a call to a native method
        TextView tv = binding.sampleText;
        // tv.setText(NativeLib.stringFromJNI());

//        MyCppRenderer mrender = new MyCppRenderer();
//        mrender.init();
//        mrender.draw();
//        mrender.draw();
//        mrender.draw();
//        mrender.draw();
    }
    /**
     * 获取支持的OpenGL版本，前16位代表主要版本，后16位代表次要版本，如0x30002，表示OpenGL 3.2
     */
    @RequiresApi(api = Build.VERSION_CODES.M)
    public int getGLVersion(){
        ActivityManager activityManager = getSystemService(ActivityManager.class);
        ConfigurationInfo info = activityManager.getDeviceConfigurationInfo();
        return info.reqGlEsVersion;
    }

    @Override
    protected void onResume() {
        super.onResume();
        // gpu_btn_call.gpuThread.continueFlag = false;
//        if(gpu_button.getText() == "停止提取") {
//            gl_view.onResume();
//        }
    }

    @Override
    protected void onPause() {
        super.onPause();
//        gl_view.onPause();
//        if(gpu_button.getText() == "停止提取"){
//            gpu_btn_call.gpuThread.continueFlag = true;
//        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        stopForegroundService(); // 停止前台服务
        // 执行其他清理工作
    }


    private void startForegroundService() {
        Intent serviceIntent = new Intent(this, MyForegroundService.class);
        startService(serviceIntent);
    }

    private void stopForegroundService() {
        Intent serviceIntent = new Intent(this, MyForegroundService.class);
        stopService(serviceIntent);
    }
}


