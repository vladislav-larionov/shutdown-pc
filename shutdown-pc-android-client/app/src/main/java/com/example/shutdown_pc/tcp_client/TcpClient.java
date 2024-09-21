package com.example.shutdown_pc.tcp_client;

import android.os.AsyncTask;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;


public class TcpClient extends AsyncTask< Void, Void, Void >
{
    private Socket socket;
    private String serverAddress = "";
    private int port = 9090;
    private OnTcpEventHandler eventListener = null;

    public TcpClient(String address, OnTcpEventHandler eventListener)
    {
        setServerAddress(address);
        this.eventListener = eventListener;
    }

    public void setServerAddress(String address)
    {
        this.serverAddress = address;
        try
        {
            if (socket != null)
                socket.close();
        } catch (IOException e)
        {
            eventListener.onChangeConnectionStatus(false);
        }
    }

    public String getServerAddress()
    {
        return serverAddress;
    }

    public void sendMessage(final String message)
    {
        Runnable runnable = new Runnable()
        {
            @Override
            public void run()
            {
                try
                {
                    if (socket == null || socket.isClosed() || !socket.isConnected()) return;
                    OutputStream output  = socket.getOutputStream();
                    PrintWriter writer = new PrintWriter(output, true);
                    writer.println(message);
                } catch (IOException e)
                {
                    eventListener.onChangeConnectionStatus(false);
                    System.err.println(e);
                }
            }
        };
        Thread thread = new Thread(runnable);
        thread.start();
    }

    protected Void doInBackground(Void...param) {
        while (true) {
            try {
                socket = new Socket(serverAddress, port);
                eventListener.onChangeConnectionStatus(true);
                InputStream input = socket.getInputStream();
                InputStreamReader reader = new InputStreamReader(input);
                int character;
                StringBuilder data = new StringBuilder();
                while ((character = reader.read()) != -1)
                {
                    data.append((char) character);
                    if (character == '\n')
                    {
                        eventListener.onMessageReceived(data.toString());
                        data.setLength(0);
                    }
                }
                socket.close();
            } catch (IOException e) {
                eventListener.onChangeConnectionStatus(false);
            }
        }
    }

    public interface OnTcpEventHandler
    {
        void onChangeConnectionStatus(boolean IsConnected);
        void onMessageReceived(String message);
    }
}
