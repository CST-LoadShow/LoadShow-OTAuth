package com.example.fingerprint;

import android.app.Dialog;
import android.content.Context;
import android.graphics.Point;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.Display;
import android.view.View;
import android.view.WindowManager;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.NonNull;

public class SettingDialog extends Dialog implements View.OnClickListener {
    private TextView mTitle, mConfirm, mCancel;
    public EditText cpu_ip, cpu_port, gpu_ip, gpu_port;

    private String title,message,confirm,cancel;

    private OnCancellistener cancellistener;
    private OnConfirmlistener confirmlistener;

    public SettingDialog(@NonNull Context context) {
        super(context);
    }

    public SettingDialog(@NonNull Context context, int themeResId) {
        super(context, themeResId);
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public void setConfirm(String confirm,OnConfirmlistener listener) {
        this.confirm = confirm;
        this.confirmlistener=listener;
    }

    public void setCancel(String cancel,OnCancellistener listener) {
        this.cancel = cancel;
        this.cancellistener=listener;
    }

    public void updateEditText(){
        cpu_ip.setText(NativeLib.CPU_IP);
        cpu_port.setText(NativeLib.CPU_PORT);
        gpu_ip.setText(NativeLib.GPU_IP);
        gpu_port.setText(NativeLib.GPU_PORT);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.setting_custom_dialog);
        //设置宽度
        WindowManager manager= getWindow().getWindowManager();
        Display display=manager.getDefaultDisplay();
        WindowManager.LayoutParams params=getWindow().getAttributes();
        Point size=new Point();
        display.getSize(size);
        params.width=(int)(size.x*0.8);
        getWindow().setAttributes(params);
        //实现圆角
        getWindow().setBackgroundDrawableResource(R.drawable.setting_dialog);

        mTitle = (TextView) findViewById(R.id.setting_title);
        mConfirm = (TextView) findViewById(R.id.setting_ok);
        mCancel = (TextView) findViewById(R.id.setting_no);

        cpu_ip = (EditText) findViewById(R.id.cpu_ip);
        cpu_port = (EditText) findViewById(R.id.cpu_port);
        gpu_ip = (EditText) findViewById(R.id.gpu_ip);
        gpu_port = (EditText) findViewById(R.id.gpu_port);
        updateEditText();

        if(TextUtils.isEmpty(title)){
            mTitle.setText(title);
        }
//        if(TextUtils.isEmpty(message)){
//            mTvMessage.setText(message);
//        }
        if(TextUtils.isEmpty(title)){
            mConfirm.setText(confirm);
        }
        if(TextUtils.isEmpty(title)){
            mCancel.setText(cancel);
        }
        mConfirm.setOnClickListener(this);
        mCancel.setOnClickListener(this);
    }

    @Override
    public void onClick(View view) {
        switch (view.getId()){
            case R.id.setting_no:
                if(cancellistener!=null){
                    cancellistener.onCancel(this);
                }
                dismiss();
                break;
            case R.id.setting_ok:
                if(confirmlistener!=null){
                    confirmlistener.onConfirm(this);
                }
                dismiss();
                break;
        }
    }

    public interface OnConfirmlistener{
        void onConfirm(SettingDialog dialog);
    }
    public interface OnCancellistener{
        void onCancel(SettingDialog dialog);
    }
}

