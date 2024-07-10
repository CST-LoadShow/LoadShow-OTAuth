package com.example.fingerprint;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.app.Activity;
import android.app.ActivityManager;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.ConfigurationInfo;

import android.os.Build;
import android.os.Bundle;

import android.view.MotionEvent;
import android.view.View;
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
    public Button ip_setting_button = null;



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

        // 获取名为"myPrefs"的SharedPreferences实例
        SharedPreferences sharedPreferences = getSharedPreferences("NETWORK_CONFIG", Context.MODE_PRIVATE);
        NativeLib.CPU_IP = sharedPreferences.getString("CPU_IP", "127.0.0.1");
        NativeLib.CPU_PORT = sharedPreferences.getString("CPU_PORT", "8888");
        NativeLib.GPU_IP = sharedPreferences.getString("GPU_IP", "127.0.0.1");
        NativeLib.GPU_PORT = sharedPreferences.getString("GPU_PORT", "8889");


        ip_setting_button = (Button)findViewById(R.id.ip_setting_btn);
        ip_setting_button.setOnTouchListener(new View.OnTouchListener() {
            private boolean isPressed = false;

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                switch (event.getAction()) {
                    case MotionEvent.ACTION_DOWN:
                        ip_setting_button.setBackgroundResource(R.mipmap.config_btn_press);
                        isPressed = true;
                        break;
                    case MotionEvent.ACTION_UP:
                        ip_setting_button.setBackgroundResource(R.mipmap.config_btn);
                        isPressed = false;
                        break;
                    case MotionEvent.ACTION_MOVE:
                        break;
                    case MotionEvent.ACTION_CANCEL:
                        if (isPressed) {
                            ip_setting_button.setBackgroundResource(R.mipmap.config_btn_press);
                        }
                        break;
                }
                return false;
            }
        });

        ip_setting_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ip_setting_button.setBackgroundResource(R.mipmap.config_btn);

                SettingDialog settingDialog=new SettingDialog(MainActivity.this);
                settingDialog.setTitle("Connetion Configuration");
                settingDialog.setConfirm("Confirm", new SettingDialog.OnConfirmlistener() {
                    @Override
                    public void onConfirm(SettingDialog dialog) {
                        NativeLib.CPU_IP = settingDialog.cpu_ip.getText().toString();
                        NativeLib.CPU_PORT = settingDialog.cpu_port.getText().toString();
                        NativeLib.GPU_IP = settingDialog.gpu_ip.getText().toString();
                        NativeLib.GPU_PORT= settingDialog.gpu_port.getText().toString();
                        settingDialog.updateEditText();
                        SharedPreferences sharedPreferences = getSharedPreferences("NETWORK_CONFIG", Context.MODE_PRIVATE);
                        SharedPreferences.Editor editor = sharedPreferences.edit();
                        editor.putString("CPU_IP", NativeLib.CPU_IP);
                        editor.putString("CPU_PORT", NativeLib.CPU_PORT);
                        editor.putString("GPU_IP", NativeLib.GPU_IP);
                        editor.putString("GPU_PORT", NativeLib.GPU_PORT);
                        editor.apply();

                    }
                });
                settingDialog.setCancel("Cancel", new SettingDialog.OnCancellistener() {
                    @Override
                    public void onCancel(SettingDialog dialog) {
                        settingDialog.updateEditText();
                    }
                });
                settingDialog.show();
            }
        });

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


