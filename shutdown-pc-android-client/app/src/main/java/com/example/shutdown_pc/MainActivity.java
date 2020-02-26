package com.example.shutdown_pc;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.DialogInterface;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import android.os.Bundle;
import android.os.Handler;
import android.os.AsyncTask;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.CheckBox;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.EditText;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import androidx.appcompat.app.AlertDialog;

public class MainActivity extends AppCompatActivity
{
    private String SERVER_ADDRESS = "http://192.168.1.44:5000";
    private String CONNECT_URL = SERVER_ADDRESS + "/connect";
    private String SHUTDOWN_URL = SERVER_ADDRESS + "/shutdown";
    private String CANCEL_SHUTDOWN_URL = SERVER_ADDRESS + "/shutdown_cancel";
    private String SHUTDOWN_AFTER_URL = SERVER_ADDRESS + "/shutdown?time=";


    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        runConnectionWithServerChecker();
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

    public boolean internetIsConnected()
    {
        ConnectivityManager connMgr = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
        NetworkInfo networkInfo = connMgr.getActiveNetworkInfo();
        return (networkInfo != null && networkInfo.isConnected());
    }

    public void onClickConnect(View view)
    {
        new ConnectTask().execute(CONNECT_URL);
    }

    private Integer readTime()
    {
        CheckBox useCustomTimeCB = (CheckBox) findViewById(R.id.useCustomTimeCB);
        EditText timeField = (EditText) findViewById(R.id.customTimeField);
        Spinner defaultTimeSpinner = (Spinner) findViewById(R.id.timeSpinner);

        String time;
        if (useCustomTimeCB.isChecked()) 
			time = timeField.getText().toString();
        else 
			time = defaultTimeSpinner.getSelectedItem().toString();

        if (time.isEmpty()) return -1;
        return ((int) (Double.parseDouble(time) * 60));
    }

    public void onClickShutdown(View view)
    {
        Integer time = readTime();
        if (time < 0) return;
        new RequestTask().execute(SHUTDOWN_AFTER_URL + time);
    }

    public void onClickUseCustomTime(View view)
    {
        CheckBox useCustomTimeCB = (CheckBox) findViewById(R.id.useCustomTimeCB);
        Spinner defaultTimeSpinner = (Spinner) findViewById(R.id.timeSpinner);
        if (useCustomTimeCB.isChecked())
        {
            setCustomTimeFieldEnabled(true);
            defaultTimeSpinner.setEnabled(false);
        }
        else
        {
            setCustomTimeFieldEnabled(false);
            defaultTimeSpinner.setEnabled(true);
        }
    }

	private void setCustomTimeFieldEnabled(boolean value)
	{
        EditText customTimeField = (EditText) findViewById(R.id.customTimeField);
        customTimeField.setFocusable(value);
        customTimeField.setClickable(value);
        customTimeField.setFocusableInTouchMode(value);
        customTimeField.setCursorVisible(value);
	}

    public void onClickCancelShutdown(View view)
    {
        new RequestTask().execute(CANCEL_SHUTDOWN_URL);
    }

    public void onClickExit(View view)
    {
        finish();
        System.exit(0);
    }

    private void setServerAddress(String ServerAddress)
    {
        if (ServerAddress == null || ServerAddress.isEmpty()) return;
        SERVER_ADDRESS = ServerAddress;
    }

    public void onServerSettingOptionsMenu(MenuItem item)
    {
        final EditText newHost = new EditText(this);
        newHost.setText(SERVER_ADDRESS);
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
                        new ConnectTask().execute(CONNECT_URL);
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

    private class ConnectTask extends RequestTask
    {
        protected void onPostExecute(String result)
        {
            if (result != null && result.equals("True"))
            {
                setStatus(true);
            }
            else
            {
                setStatus(false);
            }
        }
    }

    private class RequestTask extends AsyncTask<String, Integer, String>
    {
        @Override
        protected String doInBackground(String... path)
        {
            try
            {
                return makeRequest(path[0]);
            } catch (IOException ex)
            {
                return null;
            }
        }
    }

    private void runConnectionWithServerChecker()
    {
        final Handler handler = new Handler();
        handler.post(new Runnable()
        {
            @Override
            public void run()
            {
                new ConnectTask().execute(CONNECT_URL);
                handler.postDelayed(this, 30000);
            }
        });
    }

    private String makeRequest(String path) throws IOException
    {
        if (!internetIsConnected()) return null;

        URL url = new URL(path);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        connection.setRequestMethod("GET");
        connection.connect();
        return readAnswer(connection);
    }

    private String readAnswer(HttpURLConnection connection) throws IOException
    {
        BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
        StringBuilder buf = new StringBuilder();
        String line = null;
        while ((line = reader.readLine()) != null)
        {
            buf.append(line);
        }
        reader.close();
        return buf.toString();
    }
}
