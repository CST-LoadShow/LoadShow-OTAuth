package com.example.fingerprint;

import android.content.Context;
import android.content.Intent;
import android.opengl.GLSurfaceView;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.fingerprint.service.MyForegroundService;
import com.example.fingerprint.service.MyIntentService;
import com.example.fingerprint.service.MyService;

public class GPUButtonCall implements OnClickListener {
    private Context context;
    private boolean startFlag = false;
    GPUThread gpuThread = null;
    Button button = null;
    String text = "";
    EditText targetAppName;
    public GPUButtonCall(Context context, Button button, EditText targetAppName){
        this.context = context;
        this.button = button;
        this.text = (String) button.getText();
        this.targetAppName = targetAppName;
    }

    @Override
    public void onClick(View view){
        String s = targetAppName.getText().toString();
        if(s.equals("")){
//            targetAppName.setText("baseline");
            NativeLib.targetAppName = "-baseline";
        }else {
            NativeLib.targetAppName = "-" + targetAppName.getText();
        }
        startFlag = !startFlag;
        if(startFlag){
            button.setText("停止提取");
            Toast.makeText(context, "开始获取GPU数据",Toast.LENGTH_SHORT).show();
            if(NativeLib.serviceAppName.equals("MyIntentService")) {
                /** 服务方法 */
                NativeLib.isRunning = true;
                Intent startIntent = new Intent(context, MyIntentService.class);
                context.startService(startIntent);
            }else if(NativeLib.serviceAppName.equals("MyService")){
                Intent startIntent = new Intent(context, MyService.class);
                context.startService(startIntent);
            }else if(NativeLib.serviceAppName.equals("MyForegroundService")){
                Intent startIntent = new Intent(context, MyForegroundService.class);
                context.startService(startIntent);
            }else{
                /** 线程方法 */
                gpuThread = new GPUThread(button);
                gpuThread.isRunning = true;
                gpuThread.start();
            }


        }else{
            button.setText(text);
            gpuThread.isRunning = false;
            Toast.makeText(context, "GPU数据提取完毕",Toast.LENGTH_SHORT).show();
        }
    }
}
