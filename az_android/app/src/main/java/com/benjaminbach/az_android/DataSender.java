package com.benjaminbach.az_android;

import android.os.AsyncTask;

import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class DataSender extends AsyncTask<String, Void, Void> {
    private Exception exception;

    private String SERVER_IP = "192.168.0.151";
    private int SERVER_PORT = 8000;


    @Override
    protected Void doInBackground(String... params) {
        try {
            try {
                Socket socket = new Socket(SERVER_IP, SERVER_PORT);
                PrintWriter outToServer = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
                outToServer.print(params[0]);
                outToServer.flush();

            } catch(Exception e) {
                e.printStackTrace();
            }
        } catch(Exception e) {
            this.exception = e;
            return null;
        }

        return null;
    }

}
