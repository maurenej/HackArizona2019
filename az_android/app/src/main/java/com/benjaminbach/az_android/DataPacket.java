package com.benjaminbach.az_android;

public class DataPacket {


    public class Acceleration {
        private double x;
        private double y;
        private double z;

        double getX() {
            return x;
        }
        double getY() {
            return y;
        }
        double getZ() {
            return z;
        }

        void setX(double input) {
            x = input;
        }
        void setY(double input) {
            y = input;
        }
        void setZ(double input) {
            z = input;
        }

    }

    public class Orientation {
        private double azimuth;
        private double pitch;
        private double roll;

        public double getAzimuth() {
            return azimuth;
        }

        public double getPitch() {
            return pitch;
        }

        public double getRoll() {
            return roll;
        }

        public void setAzimuth(double input) {
            azimuth = input;
        }

        public void setPitch(double input) {
            pitch = input;
        }

        public void setRoll(double input) {
            roll = input;
        }
    }





}
