package com.example.shutdown_pc;

import android.content.DialogInterface;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.example.shutdown_pc.tcp_client.TcpClient;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity
{
    private TcpClient tcpClient;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        tcpClient = new TcpClient(new TcpClient.OnTcpEventHandler()
                {
                    @Override
                    public void onChangeConnectionStatus(final boolean IsConnected)
                    {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                setStatus(IsConnected);
                            }
                        });
                    }

                    @Override
                    public void onMessageReceived(final String message)
                    {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                            }
                        });
                    }
                });
        tcpClient.execute();
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    private void setStatus(boolean value)
    {
        TextView connectionStatus = (TextView) findViewById(R.id.connectionValueLabel);
        if (value)
        {
            connectionStatus.setText(R.string.connected);
            connectionStatus.setTextColor(getResources().getColor(R.color.connected));
        }
        else
        {
            connectionStatus.setText(R.string.disconnected);
            connectionStatus.setTextColor(getResources().getColor(R.color.disconnected));
        }
    }

    private Integer readTime()
    {
        EditText customTimeField = (EditText) findViewById(R.id.customTimeField);
        Spinner defaultTimeSpinner = (Spinner) findViewById(R.id.timeSpinner);

        String time;
        if (customTimeField.getVisibility() == View.VISIBLE)
			time = customTimeField.getText().toString();
        else 
			time = defaultTimeSpinner.getSelectedItem().toString();

        if (time.isEmpty()) return -1;
        return Integer.parseInt(time) * 60;
    }

    public void onClickShutdown(View view)
    {
        Integer time = readTime();
        if (time < 0) return;
        tcpClient.sendMessage("shutdown " + time);
    }

    public void onClickUseCustomTime(View view)
    {
        TextView useCustomTimeLabel = (TextView) findViewById(R.id.useCustomTimeLabel);
        Spinner defaultTimeSpinner = (Spinner) findViewById(R.id.timeSpinner);
        ImageButton plusBtn = (ImageButton) findViewById(R.id.plusBtn);
        ImageButton minusBtn = (ImageButton) findViewById(R.id.minusBtn);
        EditText timeField = (EditText) findViewById(R.id.customTimeField);
        useCustomTimeLabel.setVisibility(View.GONE);
        defaultTimeSpinner.setVisibility(View.GONE);
        plusBtn.setVisibility(View.GONE);
        minusBtn.setVisibility(View.GONE);
        timeField.setVisibility(View.VISIBLE);
        String time = defaultTimeSpinner.getSelectedItem().toString();
        timeField.setText(time);
    }

    public void onClickPlusBtn(View view)
    {
        Spinner defaultTimeSpinner = (Spinner) findViewById(R.id.timeSpinner);
        int curPosition = defaultTimeSpinner.getSelectedItemPosition();
        if (defaultTimeSpinner.getResources().getStringArray(R.array.time).length > curPosition + 1)
            defaultTimeSpinner.setSelection(curPosition + 1);
    }

    public void onClickMinusBtn(View view)
    {
        Spinner defaultTimeSpinner = (Spinner) findViewById(R.id.timeSpinner);
        int curPosition = defaultTimeSpinner.getSelectedItemPosition();
        if (curPosition - 1 >= 0)
            defaultTimeSpinner.setSelection(curPosition - 1);
    }

    public void onClickCancelShutdown(View view)
    {
        tcpClient.sendMessage("Cancel");
    }

    public void onClickExit(View view)
    {
        finish();
        System.exit(0);
    }

    private void setServerAddress(String serverAddress)
    {
        tcpClient.setServerAddress(serverAddress);
    }

    public void onServerSettingOptionsMenu(MenuItem item)
    {
        final EditText newHost = new EditText(this);
        newHost.setText(tcpClient.getServerAddress());
        AlertDialog.Builder builder = new AlertDialog.Builder(this)
                .setTitle(R.string.change_host_address)
                .setView(newHost)
                .setPositiveButton("OK", new DialogInterface.OnClickListener()
                {
                    @Override
                    public void onClick(DialogInterface dialog, int which)
                    {
                        dialog.dismiss();
                        setServerAddress(newHost.getText().toString());
                    }
                })
                .setNegativeButton("Cancel", new DialogInterface.OnClickListener()
                {
                    @Override
                    public void onClick(DialogInterface dialog, int which)
                    {
                        dialog.cancel();
                    }
                });
        builder.show();
    }
}
