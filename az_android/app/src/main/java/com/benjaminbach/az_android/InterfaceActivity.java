package com.benjaminbach.az_android;

import android.os.*;
import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.util.Calendar;
import java.util.HashMap;
import java.util.Map;

public class InterfaceActivity extends AppCompatActivity implements SensorEventListener {
    private SensorManager mSensorManager;
    private Sensor accelerometer1, accelerometer2, magnetic_field;

    private Handler handler;
    private boolean SEND_DATA = false;

    TextView x, y, z;
    TextView a, b, c;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);

        accelerometer1 = mSensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
        accelerometer2 = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        magnetic_field = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
        mSensorManager.registerListener(this, accelerometer1, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(this, accelerometer2, SensorManager.SENSOR_DELAY_NORMAL);
        mSensorManager.registerListener(this, magnetic_field, SensorManager.SENSOR_DELAY_NORMAL);
        x = findViewById(R.id.accel_x);
        y = findViewById(R.id.accel_y);
        z = findViewById(R.id.accel_z);
        a = findViewById(R.id.azimuth);
        b = findViewById(R.id.pitch);
        c = findViewById(R.id.roll);

        handler = new Handler();
    }



    public void beginTransfer(View v) {
        if(SEND_DATA) {
            new DataSender().execute("3292");
            handler.removeCallbacksAndMessages(null);
            SEND_DATA = false;
            return;
        }

        final int delay = 1000;
        handler.postDelayed(new Runnable(){
            @Override
            public void run(){
                for(int i = 0; i < 3; i++) {
                    if(send1[i] <= 0.0001 && send1[i] >= -0.0001)
                        send1[i] = 0;
                    if(send2[i] <= 0.0001 && send2[i] >= -0.0001)
                        send2[i] = 0;
                }
                new DataSender().execute(Double.toString(send1[0]) + " " + Double.toString(send1[1]) + " " + Double.toString(send1[2])
                        + " " + Double.toString(send2[0]) + " " + Double.toString(send2[1]) + " " + Double.toString(send2[2]));
                handler.postDelayed(this, delay);
            }
        }, delay);
        SEND_DATA = true;

    }


    public void onAccuracyChanged(Sensor sensor, int accuracy) {
    }

    private float [] acc = new float[3];
    private float [] magnet = new float[3];
    private float [] orientation = new float[3];

    private float [] send1 = new float[3];
    private float [] send2 = new float[3];

    public void onSensorChanged(SensorEvent event){

        switch (event.sensor.getType()) {

            case Sensor.TYPE_LINEAR_ACCELERATION:
                send1 = event.values.clone();
                x.setText("x: " + Double.toString(event.values[0]));
                y.setText("y: " + Double.toString(event.values[1]));
                z.setText("z: " + Double.toString(event.values[2]));
                break;

            case Sensor.TYPE_ACCELEROMETER:
                acc = event.values.clone();
                break;

            case Sensor.TYPE_MAGNETIC_FIELD:
                magnet = event.values.clone();
                break;
        }

        if (acc != null && magnet != null) {

            float R[] = new float[9];
            float I[] = new float[9];

            if (SensorManager.getRotationMatrix(R, I, acc, magnet)) {
                //orientation[] = new float[3];
                SensorManager.getOrientation(R, orientation);
                send2 = orientation.clone();
                a.setText("x: " + Double.toString(orientation[0]));
                b.setText("y: " + Double.toString(orientation[1]));
                c.setText("z: " + Double.toString(orientation[2]));
            }

            acc = null;
            magnet = null;
        }
    }


    // leave these, part of new android studio update

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
