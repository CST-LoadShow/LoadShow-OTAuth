package com.example.fingerprint;


import android.content.Context;
import android.util.Log;

import java.io.IOException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * CPU: 81.70.33.32:8 082
 * GPU: 81.70.33.32:8080
 * */

public class RemoteServer {
    public void postString(String str, String ip, String port, String append, String cur_time){

//        System.out.println("手机品牌：" + android.os.Build.BRAND);
//        System.out.println("手机型号：" + android.os.Build.MODEL);
//        System.out.println("系统版本： Android " + android.os.Build.VERSION.RELEASE);
        String device_name = android.os.Build.BRAND + " " + android.os.Build.MODEL + " " +
                android.os.Build.VERSION.RELEASE;

        String method_name = "";
        if(NativeLib.serviceAppName.equals("MyIntentService")){
            method_name = "_service";
        }else if(NativeLib.serviceAppName.equals("MyService")){
            method_name = "_service2";
        }else{
            method_name = "";
        }

        String gpu_function_name = NativeLib.GPU_FUNCTION;

        OkHttpClient client = new OkHttpClient();
        String target_url = "http://" + ip + ":" + port + append;

        RequestBody requestBody;
        // CPU
        method_name = "_OTAuth_CPU";
        requestBody = new FormBody.Builder()
                .add("device_name", device_name + method_name + NativeLib.targetAppName)
                .add("fingerprint", str)
                .build();

        // GPU
        if(append.equals("/get_offscreen_traces")){
            method_name = "_OTAuth_GPU";
            requestBody = new FormBody.Builder()
                    .add("device_name", device_name + gpu_function_name + method_name + NativeLib.targetAppName)
                    .add("trace", device_name + gpu_function_name + method_name + NativeLib.targetAppName + "," + str)
                    .add("cur_time", cur_time)
                    .build();
        }
        Request request = new Request.Builder()
                .url(target_url)
                .post(requestBody)
                .addHeader("Content-Type", "application/json")
                .addHeader("Connection", "keep-alive")
                .build();
        try {
            Response response = client.newCall(request).execute();
            response.close();
        }catch(Exception e){
            e.printStackTrace();
        }

    }

    public void send(String str, String ip, String port, String append){


    }


}
