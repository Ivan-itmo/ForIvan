package demo;

import entities.ResultEntry;
import mbeans.MBeanRegistry;

import java.lang.management.ManagementFactory;
import java.util.Date;
import java.util.Random;

public class MonitoringDemo {
    public static void main(String[] args) throws Exception {
        boolean optimized = args.length > 0 && "--optimized".equals(args[0]);
        DemoResultsStore store = new DemoResultsStore(optimized);
        Random random = new Random();
        System.out.println("Monitoring demo started");
        System.out.println("Mode: " + (optimized ? "optimized" : "slow"));
        System.out.println("PID: " + ProcessHandle.current().pid());
        System.out.println("JVM: " + ManagementFactory.getRuntimeMXBean().getName());
        System.out.println("Connect with JConsole or VisualVM. Press Ctrl+C to stop.");

        while (true) {
            double x = round(random.nextDouble() * 10.0 - 5.0);
            double y = round(random.nextDouble() * 8.0 - 3.0);
            double r = round(0.1 + random.nextDouble() * 2.9);
            boolean hit = isHit(x, y, r);
            ResultEntry entry = new ResultEntry(x, y, r, hit, new Date());
            MBeanRegistry.getPointStats().registerPoint(hit);
            MBeanRegistry.getArea().updateRadius(r);
            store.add(entry);

            if (store.getResultsCount() % 25 == 0) {
                System.out.println("results=" + store.getResultsCount()
                        + ", pointsInArea=" + store.getHitCount()
                        + ", area=" + MBeanRegistry.getArea().getArea());
            }
            Thread.sleep(250);
        }
    }

    private static boolean isHit(double x, double y, double r) {
        boolean inQuarterCircle = x <= 0 && y <= 0 && (x * x + y * y) <= r * r;
        boolean inRectangle = x <= r && x >= 0 && y <= r / 2.0 && y >= 0;
        boolean inTriangle = x <= 0 && y >= 0 && y <= 2 * x + r;
        return inQuarterCircle || inRectangle || inTriangle;
    }

    private static double round(double value) {
        return Math.round(value * 100.0) / 100.0;
    }
}
