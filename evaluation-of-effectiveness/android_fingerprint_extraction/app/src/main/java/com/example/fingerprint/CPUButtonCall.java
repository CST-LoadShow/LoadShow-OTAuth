package com.example.fingerprint;

import android.content.Context;
import android.content.Intent;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.example.fingerprint.service.MyForegroundService;
import com.example.fingerprint.service.MyIntentService;
import com.example.fingerprint.service.MyService;


public class CPUButtonCall implements OnClickListener {
    private Context context;
    private boolean startFlag = false;
    CPUThread cpuThread = null;
    Button button = null;
    String text = "";
    EditText targetAppName;
    public CPUButtonCall(Context context, Button button, EditText targetAppName){
        this.context = context;
        this.button = button;
        this.text = (String) button.getText();
        this.targetAppName = targetAppName;
    }

    @Override
    public void onClick(View view){
        String s = targetAppName.getText().toString();
        if(s.equals("")){
            // targetAppName.setText("baseline");
            NativeLib.targetAppName = "-baseline";
        }else {
            NativeLib.targetAppName = "-" + targetAppName.getText();
        }

        startFlag = !startFlag;
        // 开始测试
        if(startFlag){
            button.setText("停止提取");
            Toast.makeText(context, "开始获取CPU数据",Toast.LENGTH_SHORT).show();

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
                cpuThread = new CPUThread(button);
                cpuThread.isRunning = true;
                cpuThread.start();
            }


        // 停止测试
        }else{
            button.setText(text);
            Toast.makeText(context, "CPU数据提取完毕",Toast.LENGTH_SHORT).show();
            if(NativeLib.serviceAppName.equals("MyIntentService")) {
                /** 服务方法 */
                NativeLib.isRunning = false;
                Intent stopIntent = new Intent(context, MyIntentService.class);
                context.stopService(stopIntent); // 停止服务
            }else if(NativeLib.serviceAppName.equals("MyService")){
                Intent stopIntent = new Intent(context, MyService.class);
                context.stopService(stopIntent); // 停止服务
            }else if(NativeLib.serviceAppName.equals("MyForegroundService")){

            }else{
                /** 线程方法 */
                cpuThread.isRunning = false;
            }

        }
    }


}
