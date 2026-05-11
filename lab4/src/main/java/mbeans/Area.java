package mbeans;

public class Area implements AreaMBean {
    private double currentR = 1.0;
    private double area = calculateArea(1.0);

    @Override
    public double getCurrentR() {
        return currentR;
    }

    @Override
    public double getArea() {
        return area;
    }

    @Override
    public void updateRadius(double r) {
        currentR = r;
        area = calculateArea(r);
    }

    private double calculateArea(double r) {
        double quarterCircleArea = Math.PI * r * r / 4.0;
        double rectangleArea = r * (r / 2.0);
        double triangleArea = r * (r / 2.0) / 2.0;
        return quarterCircleArea + rectangleArea + triangleArea;
    }
}
